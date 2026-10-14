import faster_whisper
import numpy

def transcribe(audio):  # 子プロセスで動く
    segments, _ = faster_whisper.WhisperModel("large-v3-turbo", compute_type="int8").transcribe(numpy.frombuffer(audio, dtype=numpy.int16).astype(numpy.float32) / 32768, language="ja")
    return "".join(s.text for s in segments)
