import os
import whisper
import subprocess
from tqdm import tqdm
import time
from datetime import timedelta
import torch


def extract_audio_from_video(video_path, audio_path):
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path
    ]
    subprocess.run(cmd, check=True)


def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    return str(timedelta(seconds=int(seconds)))


def batch_transcribe(folder, output_folder, model_size="medium", language=None, keep_audio=False,
                     combine_transcripts=False):
    os.makedirs(output_folder, exist_ok=True)
    audio_exts = ('.wav', '.mp3', '.flac', '.m4a', '.ogg')
    video_exts = ('.mp4', '.avi', '.mov', '.mkv')
    files = [f for f in os.listdir(folder) if f.lower().endswith(audio_exts + video_exts)]

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\nUsing device: {device.upper()}")
    if device == "cuda":
        print(f"GPU detected: {torch.cuda.get_device_name(0)}")
    else:
        print("No GPU detected, using CPU.")

    model = whisper.load_model(model_size).to(device)
    transcript_segments = []
    total_start = time.time()
    per_file_times = []

    with tqdm(total=len(files), desc="Batch Progress", unit="file") as batch_bar:
        for file in files:
            input_path = os.path.join(folder, file)
            if file.lower().endswith(video_exts):
                audio_path = os.path.join(output_folder, os.path.splitext(file)[0] + "_audio.wav")
                extract_audio_from_video(input_path, audio_path)
                transcribe_path = audio_path
            else:
                transcribe_path = input_path
                audio_path = None

            print(f"\nTranscribing {file}...")
            file_start = time.time()
            try:
                result = model.transcribe(transcribe_path, language=language)
            except Exception as e:
                print(f"✗ Failed to transcribe {file}: {e}")
                batch_bar.update(1)
                continue

            file_end = time.time()
            file_time = file_end - file_start
            per_file_times.append((file, file_time))

            output_path = os.path.join(output_folder, os.path.splitext(file)[0] + "_transcript.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"Transcript for {file}\n")
                f.write(f"Processing time: {format_timestamp(file_time)}\n\n")
                for segment in result.get('segments', []):
                    start_ts = format_timestamp(segment['start'])
                    end_ts = format_timestamp(segment['end'])
                    speaker = "Speaker"
                    text = segment['text'].strip()
                    f.write(f"[{start_ts} - {end_ts}] {speaker}: {text}\n")
                    # For combined transcript, store all segment info:
                    transcript_segments.append({
                        "file": file,
                        "start": start_ts,
                        "end": end_ts,
                        "speaker": speaker,
                        "text": text
                    })
            print(f"✓ {file} transcribed in {format_timestamp(file_time)}")
            if audio_path:
                if not keep_audio:
                    os.remove(audio_path)
                    print(f"Deleted extracted audio: {audio_path}")
                else:
                    print(f"Saved extracted audio: {audio_path}")
            batch_bar.update(1)

    total_end = time.time()
    total_time = total_end - total_start

    print("\n" + "=" * 50)
    print("PROCESSING TIME REPORT")
    print("=" * 50)
    print(f"{'File':<60} {'Time Taken'}")
    print("-" * 70)
    for file, t in per_file_times:
        print(f"{file:<60} {format_timestamp(t)}")
    print("-" * 70)
    print(f"{'TOTAL TIME':<60} {format_timestamp(total_time)}")
    print("=" * 50)

    # Combine transcripts with timestamps if requested
    if combine_transcripts and transcript_segments:
        combined_path = os.path.join(output_folder, "Combined_Transcripts.txt")
        with open(combined_path, "w", encoding="utf-8") as f:
            f.write("COMBINED TRANSCRIPTS WITH TIMESTAMPS\n")
            f.write(f"Total processing time: {format_timestamp(total_time)}\n")
            f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            for seg in transcript_segments:
                f.write(
                    f"[{seg['file']}] [{seg['start']} - {seg['end']}] {seg['speaker']}: {seg['text']}\n"
                )
        print(f"\nCombined transcript saved to: {combined_path}")


if __name__ == "__main__":
    print("Local Batch Audio/Video Transcriber")
    print("============================")
    folder = input("Enter path to folder with audio/video files: ").strip().strip('"').strip("'")
    output_folder = input("Enter path for output transcripts: ").strip().strip('"').strip("'")
    language = input("Language code (e.g., 'en', 'de') or blank for auto: ").strip() or None
    model_size = input("Whisper model (tiny, base, small, medium, large) [medium]: ").strip() or "medium"
    keep_audio_input = input("Do you want to keep the extracted audio files? (y/n) [n]: ").strip().lower() or "n"
    keep_audio = keep_audio_input in ["y", "yes"]
    combine_input = input("Do you want to combine all transcripts into one file? (y/n) [n]: ").strip().lower() or "n"
    combine_transcripts = combine_input in ["y", "yes"]
    batch_transcribe(folder, output_folder, model_size, language, keep_audio, combine_transcripts)
    print("All done!")
