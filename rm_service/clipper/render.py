"""Download (yt-dlp), transcribe (faster-whisper), render 9:16 (ffmpeg).
Heavy tools are OPTIONAL: without them the pipeline writes a full plan/manifest (DRY_RUN)."""
import json, shutil, subprocess
from pathlib import Path
from .. import config

def has(tool): return shutil.which(tool) is not None

def download(url, out_dir):
    if not has("yt-dlp"): raise RuntimeError("yt-dlp not installed — see SETUP.md step 2")
    out = str(Path(out_dir) / "%(id)s.%(ext)s")
    subprocess.run(["yt-dlp", "-f", "bv+ba/b", "-o", out, url], check=True)
    return next(Path(out_dir).glob("*.*"))

def transcribe(video_path):
    """Returns [{'start','end','text'}]. Install: pip install faster-whisper"""
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise RuntimeError("faster-whisper not installed — pip install -r requirements.txt") from e
    model = WhisperModel("base", device="auto", compute_type="auto")
    segments, _ = model.transcribe(str(video_path), word_timestamps=False)
    return [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segments]

def ffmpeg_command(src, start, end, ass_path, out_path):
    """9:16 (1080x1920): blurred full-frame background + sharp centred video + burned captions."""
    vf = ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,"
          "crop=1080:1920,boxblur=20:5[bg];[b]scale=1080:-2[fg];"
          f"[bg][fg]overlay=(W-w)/2:(H-h)/2,subtitles='{ass_path}'")
    return ["ffmpeg", "-y", "-ss", str(start), "-to", str(end), "-i", str(src),
            "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out_path)]

def render(src, start, end, ass_path, out_path):
    if not has("ffmpeg"): raise RuntimeError("ffmpeg not installed — see SETUP.md step 2")
    subprocess.run(ffmpeg_command(src, start, end, ass_path, out_path), check=True)
    return out_path

def plan_clip(video, moment):
    """What WOULD be rendered — used in DRY_RUN so you can approve before anything posts."""
    return {"video": video, "moment": moment, "ratio": "9:16 (1080x1920)",
            "captions": "pro word-highlight ASS", "status": "planned (DRY_RUN)"}
