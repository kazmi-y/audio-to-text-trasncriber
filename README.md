# audio-to-text-transcriber
Extract audio files from videos and convert audios into text files

# 📝 Local Batch Audio/Video Transcriber

A command-line tool that uses [OpenAI Whisper](https://github.com/openai/whisper) to **batch transcribe audio and video files locally**.  
Supports multiple formats, GPU acceleration, per-file timestamps, and an optional combined transcript output.

---

## 📌 Features

- **Batch Processing** — Transcribe all supported audio and video files in a folder.
- **Automatic Audio Extraction** — Extracts audio from video files via `ffmpeg` (16 kHz mono PCM).
- **Multi-format Support** —  
  - Audio: `.wav`, `.mp3`, `.flac`, `.m4a`, `.ogg`  
  - Video: `.mp4`, `.avi`, `.mov`, `.mkv`
- **Whisper Model Selection** — Choose from `tiny`, `base`, `small`, `medium`, `large`.
- **Language Control** — Auto-detect or specify language (e.g., `en`, `de`).
- **Timestamps per Segment** — Each transcript entry is time-aligned.
- **Combined Transcript Option** — Merge all transcripts into one file.
- **GPU Acceleration** — Runs on CUDA if available.
- **Progress Tracking** — Shows batch progress and per-file timing.
- **Audio Retention Option** — Keep or delete extracted `.wav` files.

---

## 📂 Repository Structure

.
├── Local-transcriber.py # Main transcription script
├── README.md # Project documentation
└── requirements.txt # Python dependencies

text

---

## ⚙️ Installation

### 1️⃣ Prerequisites
- **Python** 3.8+
- **pip** package manager
- **ffmpeg**
  - **Linux**: `sudo apt install ffmpeg`
  - **macOS**: `brew install ffmpeg`
  - **Windows**: Download from https://ffmpeg.org and add to PATH
- **(Optional)** CUDA-enabled GPU for faster transcription

### 2️⃣ Install Dependencies

pip install -r requirements.txt

text

---

## ▶️ Usage

Run the script:

python Local-transcriber.py

text

Follow the prompts:

1. **Path to media folder** — Directory with `.mp3`, `.mp4`, etc.
2. **Output folder** — Where `.txt` transcripts are stored.
3. **Language Code** — e.g. `en` for English (blank for auto).
4. **Model Size** — `tiny` / `base` / `small` / `medium` / `large` (default: medium).
5. **Keep Extracted Audio?** — `y` or `n`.
6. **Combine Transcripts?** — `y` or `n`.

### Example
Enter path to folder with audio/video files: /home/user/media
Enter path for output transcripts: /home/user/output
Language code (e.g., 'en', 'de') or blank for auto:
Whisper model (tiny, base, small, medium, large) [medium]: small
Do you want to keep the extracted audio files? (y/n) [n]: n
Do you want to combine all transcripts into one file? (y/n) [n]: y

text

---

## 📄 Output

**Per-file transcript**  
Transcript for meeting.mp4
Processing time: 00:01:32

[00:00:00 - 00:00:06] Speaker: Hello everyone, welcome to today's meeting.
[00:00:06 - 00:00:12] Speaker: Let's start with project updates.

text

**Optional combined file:**  
Combined_Transcripts.txt
COMBINED TRANSCRIPTS WITH TIMESTAMPS
Total processing time: 00:15:43
Generated on: 2025-08-13
[meeting.mp4] [00:00:00 - 00:00:06] Speaker: Hello everyone, welcome...

text

---

## 💡 Tips

- **Fast drafts** → `tiny`/`base`  
  **Better accuracy** → `medium`/`large`
- **GPU acceleration:** Install PyTorch with matching CUDA:
pip install torch --index-url https://download.pytorch.org/whl/cu118

text
- Run in background:
nohup python Local-transcriber.py &

text

---

## 🛠 Known Limitations

- CPU-only mode can be slow.
- No speaker diarization — all lines are labeled `Speaker`.
- Large video files take more audio-extraction time.

---

## 📜 License

MIT License — free to use and modify.

---

## 🤝 Contributing

Pull requests and ideas welcome:
- Add VTT/SRT subtitle export
- Implement speaker diarization
- Parallel processing
- GUI frontend
