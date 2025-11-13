"""
Configuration settings for YouTube Whisper Transcription
"""
import os
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / "downloads"
OUTPUTS_DIR = BASE_DIR / "outputs"

# Ensure directories exist
DOWNLOADS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

# Whisper model settings
# Available models: tiny, base, small, medium, large-v2, large-v3
# Larger models are more accurate but slower
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "large-v3")

# GPU settings for NVIDIA A6000
USE_GPU = True  # Set to False to use CPU
DEVICE = "cuda" if USE_GPU else "cpu"

# FP16 computation (requires GPU, faster but slightly less accurate)
# The A6000 supports FP16 very well
USE_FP16 = True if USE_GPU else False

# Transcription settings
LANGUAGE = None  # Auto-detect language, or set to 'en', 'es', etc.
TASK = "transcribe"  # "transcribe" or "translate" (to English)

# Output format settings
OUTPUT_FORMATS = ["txt", "srt", "vtt", "json"]  # Available: txt, srt, vtt, json, tsv

# yt-dlp download settings
AUDIO_FORMAT = "mp3"
AUDIO_QUALITY = "192"  # kbps

# Batch processing
BATCH_SIZE = 1  # Number of videos to process simultaneously
MAX_WORKERS = 1  # For parallel processing (be careful with GPU memory)

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
