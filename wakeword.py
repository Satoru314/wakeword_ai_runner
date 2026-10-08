"""マイクの音量をリアルタイムでバー表示する。Ctrl+C で終了。"""

import subprocess
import openwakeword 
import numpy

def start_maiku():
    return subprocess.Popen(
        ["parecord", "--raw", "--format=s16le", "--rate=16000", "--channels=1"],
        stdout=subprocess.PIPE,
    )

proc = start_maiku()
model = openwakeword.model.Model(inference_framework="onnx")

while True:
    chunk = proc.stdout.read(2560)  # 0.1秒分
    samples = numpy.frombuffer(chunk, dtype=numpy.int16)
    prediction = model.predict(samples)
    if prediction['hey_jarvis'] > 0.5:
        print("検出！", prediction['hey_jarvis'])
        subprocess.Popen(["paplay", "決定ボタンを押す2.wav"])

        audio = b""
        silent = 0
        voiced = 0
        while True:
            print(silent)
            chunk = proc.stdout.read(2560)
            audio += chunk
            if numpy.abs(numpy.frombuffer(chunk, dtype=numpy.int16)).max() < 200:
                silent += 1
            else:
                silent = 0
                voiced += 1
            if silent >= 12 and len(audio) >= 2560 * 37:
                break
        subprocess.Popen(["paplay", "カーソル移動4.wav"])
        if voiced >= 5:
            print("再生開始！")
            subprocess.run(["paplay", "--raw", "--format=s16le", "--rate=16000", "--channels=1"], input=audio)
        else:
            print("音声が認識できない")
        
        model.reset()
        proc.kill()
        proc.wait()
        proc = start_maiku()
        


    
