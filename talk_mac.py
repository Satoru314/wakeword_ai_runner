import subprocess
import numpy
from faster_whisper import WhisperModel

model = WhisperModel("large-v3-turbo", compute_type="int8")
print("録音中（10秒）")
raw = subprocess.run(
    ["rec", "-V1", "-q", "-t", "raw", "-b", "16", "-e", "signed", "-r", "16000", "-c", "1", "-", "trim", "0", "10"],
    stdout=subprocess.PIPE,
).stdout
audio = numpy.frombuffer(raw, dtype=numpy.int16).astype(numpy.float32) / 32768
segments, _ = model.transcribe(audio, language="ja")
text = "".join(s.text for s in segments)
print("あなた:", text)

reply = subprocess.run(
    ["claude", "-p", text, "--append-system-prompt", "返事は音声で読み上げられる。短い話し言葉で、記号やMarkdownを使わずに答えること。"],
    capture_output=True, text=True,
).stdout
print("Claude:", reply)
# subprocess.run(["say", reply])
