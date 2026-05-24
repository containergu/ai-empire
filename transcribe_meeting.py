import gc, os, wave, sys
import numpy as np
from faster_whisper import WhisperModel

# Tiny model — this machine can't sustain base for 3hr without OOM
model = WhisperModel("tiny", device="cpu", compute_type="int8")
print("Model loaded (tiny)", flush=True)

chunks_dir = "C:\\Users\\robin\\OneDrive\\Desktop\\George Learning AI\\Cursor Claude\\hccs-board\\chunks"
output_path = "C:\\Users\\robin\\OneDrive\\Desktop\\George Learning AI\\Cursor Claude\\hccs-board\\transcript.txt"
subchunk_dir = os.path.join(chunks_dir, "subchunks")
os.makedirs(subchunk_dir, exist_ok=True)

# 30-second sub-chunks to keep memory pressure low
SAMPLES_PER_SUB = 30 * 16000

all_text = []
for i in range(6):
    chunk_txt = os.path.join(chunks_dir, f"chunk_{i:02d}.txt")
    chunk_wav = os.path.join(chunks_dir, f"chunk_{i:02d}.wav")

    if os.path.exists(chunk_txt):
        with open(chunk_txt, "r", encoding="utf-8") as f:
            text = f.read()
        all_text.append(text)
        print(f"Chunk {i} already done, skipped ({len(text)} chars)", flush=True)
        continue

    if not os.path.exists(chunk_wav):
        print(f"Chunk {i} wav not found, stopping", flush=True)
        break

    print(f"Reading chunk {i}...", flush=True)

    with wave.open(chunk_wav, "rb") as wf:
        sampwidth = wf.getsampwidth()
        nchannels = wf.getnchannels()
        raw = wf.readframes(wf.getnframes())

    dtype = np.int16 if sampwidth == 2 else np.int32
    audio_data = np.frombuffer(raw, dtype=dtype)
    if nchannels > 1:
        audio_data = audio_data.reshape(-1, nchannels).mean(axis=1).astype(dtype)

    sub_texts = []
    for sub_idx, start in enumerate(range(0, len(audio_data), SAMPLES_PER_SUB)):
        end = min(start + SAMPLES_PER_SUB, len(audio_data))
        seg = audio_data[start:end]

        sub_name = f"chunk_{i:02d}_{sub_idx:02d}.wav"
        sub_path = os.path.join(subchunk_dir, sub_name)

        with wave.open(sub_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(seg.tobytes())

        print(f"  Chunk {i} part {sub_idx} ({start//16000}s-{end//16000}s)...", flush=True)
        try:
            segments, info = model.transcribe(sub_path, beam_size=5)
            text = " ".join(seg.text for seg in segments)
        except Exception as e:
            print(f"  ERROR: {e}", flush=True)
            text = ""

        sub_texts.append(text)
        print(f"  -> {len(text)} chars", flush=True)

        os.remove(sub_path)
        del seg, sub_path, sub_name
        gc.collect()

    full_text = " ".join(sub_texts)
    with open(chunk_txt, "w", encoding="utf-8") as f:
        f.write(full_text)
    all_text.append(full_text)
    print(f"Chunk {i} done: {len(full_text)} chars", flush=True)

    del audio_data, raw, sub_texts
    gc.collect()

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(all_text))
print(f"ALL DONE. Total: {sum(len(t) for t in all_text)} chars", flush=True)
