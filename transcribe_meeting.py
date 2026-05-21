import gc, os
from faster_whisper import WhisperModel

model = WhisperModel("tiny", device="cpu", compute_type="int8")
print("Model loaded", flush=True)

chunks_dir = "C:\\Users\\robin\\OneDrive\\Desktop\\George Learning AI\\Cursor Claude\\hccs-board\\chunks"
output_path = "C:\\Users\\robin\\OneDrive\\Desktop\\George Learning AI\\Cursor Claude\\hccs-board\\transcript.txt"

all_text = []
for i in range(6):
    audio = os.path.join(chunks_dir, f"chunk_{i:02d}.wav")
    print(f"Transcribing chunk {i}...", flush=True)
    segments, info = model.transcribe(audio, beam_size=5)
    text = " ".join(seg.text for seg in segments)
    chunk_path = os.path.join(chunks_dir, f"chunk_{i:02d}.txt")
    with open(chunk_path, "w", encoding="utf-8") as f:
        f.write(text)
    all_text.append(text)
    print(f"Chunk {i} done: {len(text)} chars", flush=True)
    gc.collect()

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(all_text))
print(f"ALL DONE. Total: {sum(len(t) for t in all_text)} chars", flush=True)
