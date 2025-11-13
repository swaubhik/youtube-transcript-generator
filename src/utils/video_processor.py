"""
Video download and processing utilities
"""
import os
import logging
from pathlib import Path
from typing import Optional, Dict

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


def get_video_info(url: str) -> Dict:
    """
    Get video information without downloading
    
    Args:
        url: YouTube video URL
    
    Returns:
        Dictionary with video metadata
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    
    return info


def download_audio(
    url: str,
    output_dir: Path,
    audio_format: str = "mp3",
    audio_quality: str = "192"
) -> str:
    """
    Download audio from YouTube video
    
    Args:
        url: YouTube video URL
        output_dir: Directory to save audio file
        audio_format: Audio format (mp3, m4a, wav, etc.)
        audio_quality: Audio quality in kbps
    
    Returns:
        Path to downloaded audio file
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Generate output template
    output_template = str(output_dir / "%(id)s.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': audio_quality,
        }],
        'outtmpl': output_template,
        'quiet': False,
        'no_warnings': False,
    }
    
    logger.info(f"Downloading audio from: {url}")
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info['id']
        audio_path = output_dir / f"{video_id}.{audio_format}"
    
    logger.info(f"Audio downloaded to: {audio_path}")
    return str(audio_path)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename
