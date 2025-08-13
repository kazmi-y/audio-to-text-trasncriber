# audio-to-text-transcriber
Extract audio files from videos and convert audios into text files

📝 Local Batch Audio/Video Transcriber
A command-line tool that uses OpenAI Whisper to batch transcribe audio and video files locally.
Supports multiple formats, GPU acceleration, per-file timestamps, and an optional combined transcript output.

📌 Features
Batch Processing — Transcribe all supported audio and video files in a folder.

Automatic Audio Extraction — Extracts audio from video files via ffmpeg with proper normalization (16 kHz mono PCM).

Multi-format Support —

Audio: .wav, .mp3, .flac, .m4a, .ogg

Video: .mp4, .avi, .mov, .mkv

Whisper Model Selection — Choose from tiny, base, small, medium, large.

Language Control — Auto-detect or specify language (e.g., en, de).

Timestamps per Segment — Each transcript entry is time-aligned.

Combined Transcript Option — Merge all per-file transcripts into a single output file.

GPU Acceleration — Runs on CUDA if available, otherwise CPU.

Progress Tracking — Shows batch progress and per-file status with timing reports.

Audio Retention Option — Keep or delete extracted audio files.

📂 Repository Structure
text
.
├── Local-transcriber.py   # Main transcription script
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
⚙️ Installation
1️⃣ Prerequisites
Python 3.8+

pip package manager

ffmpeg installed on your system

Linux: sudo apt install ffmpeg

macOS: brew install ffmpeg

Windows: Install from https://ffmpeg.org, and add it to PATH.

GPU (Optional) CUDA-enabled GPU for faster transcription

2️⃣ Install Dependencies
bash
pip install -r requirements.txt
requirements.txt should include:

text
whisper
torch
tqdm
▶️ Usage
Run the script:

bash
python Local-transcriber.py
Follow the prompts in the terminal:

Enter path to folder with files — The directory containing the audio/video files you want to transcribe.

Enter path for output — Where transcript .txt files will be saved.

Language Code — Example: en for English, de for German. Leave blank for auto-detection.

Model Size — Choose from: tiny, base, small, medium, large (default: medium).

Keep Extracted Audio? — y to keep .wav audio extracted from videos, n to delete after transcription.

Combine Transcripts? — y to combine all transcripts into one file with timestamps.

Example Run
text
Local Batch Audio/Video Transcriber
============================
Enter path to folder with audio/video files: /home/user/media
Enter path for output transcripts: /home/user/output
Language code (e.g., 'en', 'de') or blank for auto:
Whisper model (tiny, base, small, medium, large) [medium]: small
Do you want to keep the extracted audio files? (y/n) [n]: n
Do you want to combine all transcripts into one file? (y/n) [n]: y
📄 Output
For each file, the tool generates:

text
Transcript for example_video.mp4
Processing time: 00:01:32

[00:00:00 - 00:00:06] Speaker: Hello everyone, welcome to today's meeting.
[00:00:06 - 00:00:12] Speaker: Let's start with the project updates.
...
If Combine Transcripts is enabled, you'll also get:

text
Combined_Transcripts.txt

COMBINED TRANSCRIPTS WITH TIMESTAMPS
Total processing time: 00:15:43
Generated on: 2025-08-13
================================================================================
[example_video.mp4] [00:00:00 - 00:00:06] Speaker: Hello everyone, welcome...
[example_audio.mp3] [00:00:00 - 00:00:04] Speaker: This is an audio-only clip...
...
💡 Tips
Speed vs Accuracy:

Use tiny or base for quick drafts.

Use medium or large for better accuracy.

GPU Boost: Install torch with CUDA support to leverage your GPU and significantly speed up transcriptions:

bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
Background Processing: You can run it in the background for long jobs:

bash
nohup python Local-transcriber.py &
🛠 Known Limitations
Whisper can be CPU intensive and slow without GPU.

Output speaker labels are currently generic (Speaker) — no speaker diarization.

Large video files may take extra preprocessing time for audio extraction.

📜 License
This project is licensed under the MIT License — feel free to modify and use it in your projects.

🤝 Contributing
Contributions are welcome!
Ideas for improvements:

Speaker diarization

VTT/SRT subtitle export

Parallel multi-file processing

GUI frontend

If you like this project, don’t forget to ⭐ star the repository!
