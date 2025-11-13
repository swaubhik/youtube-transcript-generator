"""
File handling utilities for saving transcripts
"""
import json
import logging
from pathlib import Path
from typing import List, Dict
from datetime import timedelta

from src.utils.video_processor import sanitize_filename

logger = logging.getLogger(__name__)


def format_timestamp(seconds: float, format_type: str = "srt") -> str:
    """
    Format timestamp for subtitle files
    
    Args:
        seconds: Time in seconds
        format_type: Format type ('srt' or 'vtt')
    
    Returns:
        Formatted timestamp string
    """
    td = timedelta(seconds=seconds)
    hours = int(td.total_seconds() // 3600)
    minutes = int((td.total_seconds() % 3600) // 60)
    secs = int(td.total_seconds() % 60)
    millis = int((td.total_seconds() % 1) * 1000)
    
    if format_type == "srt":
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    elif format_type == "vtt":
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
    else:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def save_as_txt(result: Dict, output_path: Path) -> None:
    """Save transcript as plain text"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result['text'].strip())
    logger.info(f"Saved TXT: {output_path}")


def save_as_srt(result: Dict, output_path: Path) -> None:
    """Save transcript as SRT subtitle file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(result['segments'], 1):
            start = format_timestamp(segment['start'], 'srt')
            end = format_timestamp(segment['end'], 'srt')
            text = segment['text'].strip()
            
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")
    logger.info(f"Saved SRT: {output_path}")


def save_as_vtt(result: Dict, output_path: Path) -> None:
    """Save transcript as VTT subtitle file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("WEBVTT\n\n")
        for segment in result['segments']:
            start = format_timestamp(segment['start'], 'vtt')
            end = format_timestamp(segment['end'], 'vtt')
            text = segment['text'].strip()
            
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")
    logger.info(f"Saved VTT: {output_path}")


def save_as_json(result: Dict, output_path: Path) -> None:
    """Save full transcript data as JSON"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved JSON: {output_path}")


def save_as_tsv(result: Dict, output_path: Path) -> None:
    """Save transcript as TSV (tab-separated values)"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("start\tend\ttext\n")
        for segment in result['segments']:
            start = segment['start']
            end = segment['end']
            text = segment['text'].strip().replace('\t', ' ')
            f.write(f"{start:.2f}\t{end:.2f}\t{text}\n")
    logger.info(f"Saved TSV: {output_path}")


def save_transcript(
    result: Dict,
    video_id: str,
    video_title: str,
    output_dir: Path,
    formats: List[str]
) -> Dict[str, str]:
    """
    Save transcript in multiple formats
    
    Args:
        result: Whisper transcription result
        video_id: YouTube video ID
        video_title: Video title
        output_dir: Output directory
        formats: List of formats to save (txt, srt, vtt, json, tsv)
    
    Returns:
        Dictionary mapping format to output file path
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Create sanitized filename base
    safe_title = sanitize_filename(video_title)
    base_filename = f"{video_id}_{safe_title}"
    
    output_files = {}
    
    format_handlers = {
        'txt': save_as_txt,
        'srt': save_as_srt,
        'vtt': save_as_vtt,
        'json': save_as_json,
        'tsv': save_as_tsv,
    }
    
    for fmt in formats:
        if fmt in format_handlers:
            output_path = output_dir / f"{base_filename}.{fmt}"
            format_handlers[fmt](result, output_path)
            output_files[fmt] = str(output_path)
        else:
            logger.warning(f"Unknown format: {fmt}")
    
    return output_files


def clean_downloads(download_dir: Path, keep_files: List[str] = None) -> None:
    """
    Clean up downloaded files
    
    Args:
        download_dir: Directory containing downloads
        keep_files: List of file paths to keep
    """
    download_dir = Path(download_dir)
    keep_files = set(keep_files or [])
    
    if not download_dir.exists():
        return
    
    for file_path in download_dir.glob("*"):
        if file_path.is_file() and str(file_path) not in keep_files:
            try:
                file_path.unlink()
                logger.info(f"Deleted: {file_path}")
            except Exception as e:
                logger.warning(f"Could not delete {file_path}: {e}")
