# 视觉程序性能测量练习

对应《技术选型与原型》任务四。程序读取一张固定图像，转成灰度、按阈值生成掩膜，然后写出掩膜与统计结果。请先测量基线，再只改动一个环节。

## 运行基线

在 Ubuntu 或 WSL 的仓库根目录执行。使用 Python 3.10–3.13。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m vision --output-dir runs/before --repeat 5
```

首次运行会生成固定的 1280 × 720 图像 `runs/fixtures/vision-sample.png`。以后运行复用该文件。计时包括读取、灰度转换、阈值处理和写出这四个环节，默认先预热 1 次，再测 5 次。程序打印各环节及全流程的中位数（毫秒），各次原始计时保存在 `timings.csv`。生成输入和写出计时日志在计时范围之外。

## 对照实验

完成一项改动后，使用同一设备、输入和重复次数，将结果写到另一个目录。

```bash
python -m vision --output-dir runs/after --repeat 5
diff -u runs/before/stats.json runs/after/stats.json
```

两个目录均有 `mask.png` 和 `stats.json`。统计包含图像宽高、选中像素数和掩膜原始像素的 SHA-256。上面的 `diff` 若无输出，表示这些内容一致。计时波动较大时，可以增加重复次数，但前后两轮要使用同一口径。

## 提交

先在 GitHub 上 Fork 本仓库，在自己的 Fork 里创建工作分支。完成后从该分支向原仓库的 `main` 发起 PR，并将 PR 链接填入飞书问卷。组长在 PR 中验收和反馈，验收后关闭 PR。

即使决定放弃优化，也把实验改动留在 PR 分支上，方便组长核对改动。优化前后计时、输出比较和是否采用的理由按飞书问卷中的题目提交。
