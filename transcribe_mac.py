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
print("".join(s.text for s in segments))
