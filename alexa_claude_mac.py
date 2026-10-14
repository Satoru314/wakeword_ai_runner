"""「アレクサ」で起動して、話した内容を Claude に投げて返事を表示する。Ctrl+C で終了。"""

import subprocess
import openwakeword
import numpy
from faster_whisper import WhisperModel

def start_maiku():
    return subprocess.Popen(
        ["rec", "-V1", "-q", "-t", "raw", "-b", "16", "-e", "signed", "-r", "16000", "-c", "1", "-"],
        stdout=subprocess.PIPE,
    )

whisper = WhisperModel("large-v3-turbo", compute_type="int8")
proc = start_maiku()
model = openwakeword.model.Model(inference_framework="onnx")

while True:
    chunk = proc.stdout.read(2560)  # 0.1秒分
    samples = numpy.frombuffer(chunk, dtype=numpy.int16)
    prediction = model.predict(samples)
    print(prediction['alexa'])
    if prediction['alexa'] > 0.5:
        print("検出！", prediction['alexa'])
        subprocess.Popen(["afplay", "決定ボタンを押す2.wav"])

        audio = b""
        silent = 0
        voiced = 0
        while True:
            chunk = proc.stdout.read(2560)
            audio += chunk
            if numpy.abs(numpy.frombuffer(chunk, dtype=numpy.int16)).max() < 2500:  # Mac のマイクは無音でも 1000〜2500 くらいある
                silent += 1
            else:
                silent = 0
                voiced += 1
            if silent >= 12 and len(audio) >= 2560 * 37:
                break

        subprocess.Popen(["afplay", "カーソル移動4.wav"])
        if voiced >= 5:
            segments, _ = whisper.transcribe(numpy.frombuffer(audio, dtype=numpy.int16).astype(numpy.float32) / 32768, language="ja")
            text = "".join(s.text for s in segments)
            print("あなた:", text)

            reply = subprocess.run(
                ["claude", "-p", text, "--append-system-prompt", "返事は音声で読み上げられる。短い話し言葉で、記号やMarkdownを使わずに答えること。"],
                capture_output=True, text=True,
            ).stdout
            print("Claude:", reply)
            subprocess.run(["say", reply])
        else:
            print("音声が認識できない")

        model.reset()
        proc.kill()
        proc.wait()
        proc = start_maiku()
