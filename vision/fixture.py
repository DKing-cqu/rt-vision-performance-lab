from pathlib import Path

import cv2
import numpy as np


def write_fixture(path: Path) -> None:
    """Write the same 1280 × 720 test image on every run."""
    rng = np.random.default_rng(20261115)
    image = rng.integers(0, 256, size=(720, 1280, 3), dtype=np.uint8)
    cv2.circle(image, (385, 360), 140, (0, 140, 255), -1, cv2.LINE_8)
    cv2.rectangle(image, (690, 170), (1110, 470), (190, 190, 190), -1, cv2.LINE_8)
    cv2.rectangle(image, (760, 510), (1030, 635), (35, 30, 25), -1, cv2.LINE_8)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(path), image):
        raise OSError(f"Cannot write fixture: {path}")
