import argparse
import csv
from pathlib import Path
from statistics import median

from .fixture import write_fixture
from .pipeline import STAGES, run


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark an image thresholding pipeline.")
    parser.add_argument("--input", type=Path, default=Path("runs/fixtures/vision-sample.png"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--repeat", type=int, default=5)
    args = parser.parse_args()
    if args.repeat < 1:
        parser.error("--repeat must be at least 1")

    try:
        if not args.input.exists() and args.input == parser.get_default("input"):
            write_fixture(args.input)

        args.output_dir.mkdir(parents=True, exist_ok=True)
        run(args.input, args.output_dir)
        measurements = [run(args.input, args.output_dir) for _ in range(args.repeat)]
        stages = (*STAGES, "total")
        with (args.output_dir / "timings.csv").open("w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(("run", *(f"{stage}_ms" for stage in stages)))
            for index, measurement in enumerate(measurements, start=1):
                writer.writerow((index, *(f"{measurement[stage]:.3f}" for stage in stages)))
    except OSError as error:
        parser.exit(1, f"{error}\n")

    for stage in stages:
        print(f"{stage:>10}: {median(row[stage] for row in measurements):8.3f} ms (median)")


if __name__ == "__main__":
    main()
