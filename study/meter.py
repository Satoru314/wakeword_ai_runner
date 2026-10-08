"""マイクの音量をリアルタイムでバー表示する。Ctrl+C で終了。"""

import array
import subprocess

proc = subprocess.Popen(
    ["parecord", "--raw", "--format=s16le", "--rate=16000", "--channels=1"],
    stdout=subprocess.PIPE,
)

while True:
    chunk = proc.stdout.read(3200)  # 0.1秒分
    samples = array.array("h", chunk)
    peak = max(abs(s) for s in samples)
    print(f"{peak:6d} " + "#" * (peak // 200), flush=True)
