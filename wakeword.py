"""マイクの音量をリアルタイムでバー表示する。Ctrl+C で終了。"""

import array
import subprocess
import openwakeword 

proc = subprocess.Popen(
    ["parecord", "--raw", "--format=s16le", "--rate=16000", "--channels=1"],
    stdout=subprocess.PIPE,
)
model = openwakeword.model.Model()

while True:
    chunk = proc.stdout.read(2560)  # 0.1秒分
    samples = array.array("h", chunk)
    prediction = model.predict(samples)
    if prediction['hey_jarvis'] > 0.5:
        print("検出！", prediction['hey_jarvis'])
        audio = proc.stdout.read(32000 * 5)
        print("再生開始！")
        subprocess.run(["paplay", "--raw", "--format=s16le", "--rate=16000", "--channels=1"], input=audio)
        


    
