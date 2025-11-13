"""
Main script for YouTube video transcription using OpenAI Whisper
"""
import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Optional, List

import whisper
import torch
from yt_dlp import YoutubeDL

import config
from src.utils.logger import setup_logger
from src.utils.file_handler import save_transcript, clean_downloads
from src.utils.video_processor import download_audio, get_video_info

# Setup logging
logger = setup_logger(__name__, config.LOG_LEVEL)


class YouTubeTranscriber:
    """
    Main class for transcribing YouTube videos using Whisper
    """
    
    def __init__(
        self,
        model_name: str = config.WHISPER_MODEL,
        device: str = config.DEVICE,
        use_fp16: bool = config.USE_FP16
    ):
        """
        Initialize the transcriber with specified model and device settings
        
        Args:
            model_name: Whisper model to use (tiny, base, small, medium, large-v2, large-v3)
            device: Device to run on ('cuda' or 'cpu')
            use_fp16: Whether to use FP16 precision (faster on GPU)
        """
        self.model_name = model_name
        self.device = device
        self.use_fp16 = use_fp16 and device == "cuda"
        
        logger.info(f"Initializing Whisper model: {model_name}")
        logger.info(f"Device: {device}")
        logger.info(f"FP16: {self.use_fp16}")
        
        # Check GPU availability
        if device == "cuda" and not torch.cuda.is_available():
            logger.warning("CUDA not available, falling back to CPU")
            self.device = "cpu"
            self.use_fp16 = False
        
        if self.device == "cuda":
            logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
            logger.info(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        
        # Load Whisper model
        self.model = whisper.load_model(model_name, device=self.device)
        logger.info("Model loaded successfully")
    
    def transcribe_audio(
        self,
        audio_path: str,
        language: Optional[str] = config.LANGUAGE,
        task: str = config.TASK
    ) -> dict:
        """
        Transcribe an audio file using Whisper
        
        Args:
            audio_path: Path to the audio file
            language: Language code (e.g., 'en', 'es') or None for auto-detect
            task: 'transcribe' or 'translate'
        
        Returns:
            Dictionary containing transcription results
        """
        logger.info(f"Transcribing: {audio_path}")
        
        options = {
            "task": task,
            "fp16": self.use_fp16,
        }
        
        if language:
            options["language"] = language
        
        result = self.model.transcribe(audio_path, **options)
        
        logger.info(f"Transcription complete. Detected language: {result.get('language', 'unknown')}")
        return result
    
    def process_youtube_url(
        self,
        url: str,
        output_formats: List[str] = config.OUTPUT_FORMATS,
        keep_audio: bool = False
    ) -> dict:
        """
        Download and transcribe a YouTube video
        
        Args:
            url: YouTube video URL
            output_formats: List of output formats (txt, srt, vtt, json)
            keep_audio: Whether to keep the downloaded audio file
        
        Returns:
            Dictionary with transcription results and metadata
        """
        try:
            # Get video info
            video_info = get_video_info(url)
            video_id = video_info.get('id', 'unknown')
            video_title = video_info.get('title', 'unknown')
            
            logger.info(f"Processing: {video_title}")
            
            # Download audio
            audio_path = download_audio(url, config.DOWNLOADS_DIR)
            
            # Transcribe
            result = self.transcribe_audio(audio_path)
            
            # Save outputs
            output_files = save_transcript(
                result,
                video_id,
                video_title,
                config.OUTPUTS_DIR,
                output_formats
            )
            
            # Cleanup
            if not keep_audio:
                try:
                    os.remove(audio_path)
                    logger.info(f"Removed temporary audio file: {audio_path}")
                except Exception as e:
                    logger.warning(f"Could not remove audio file: {e}")
            
            return {
                "video_id": video_id,
                "video_title": video_title,
                "language": result.get("language"),
                "output_files": output_files,
                "audio_path": audio_path if keep_audio else None
            }
        
        except Exception as e:
            logger.error(f"Error processing {url}: {e}", exc_info=True)
            raise
    
    def process_batch(
        self,
        urls: List[str],
        output_formats: List[str] = config.OUTPUT_FORMATS,
        keep_audio: bool = False
    ) -> List[dict]:
        """
        Process multiple YouTube URLs
        
        Args:
            urls: List of YouTube video URLs
            output_formats: List of output formats
            keep_audio: Whether to keep downloaded audio files
        
        Returns:
            List of result dictionaries
        """
        results = []
        for i, url in enumerate(urls, 1):
            logger.info(f"Processing video {i}/{len(urls)}")
            try:
                result = self.process_youtube_url(url, output_formats, keep_audio)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process {url}: {e}")
                results.append({"url": url, "error": str(e)})
        
        return results


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Transcribe YouTube videos using OpenAI Whisper"
    )
    parser.add_argument(
        "url",
        nargs="+",
        help="YouTube video URL(s) to transcribe"
    )
    parser.add_argument(
        "--model",
        default=config.WHISPER_MODEL,
        choices=["tiny", "base", "small", "medium", "large-v2", "large-v3"],
        help="Whisper model to use"
    )
    parser.add_argument(
        "--language",
        default=config.LANGUAGE,
        help="Language code (e.g., 'en', 'es') or auto-detect if not specified"
    )
    parser.add_argument(
        "--task",
        default=config.TASK,
        choices=["transcribe", "translate"],
        help="Task: transcribe or translate to English"
    )
    parser.add_argument(
        "--output-formats",
        nargs="+",
        default=config.OUTPUT_FORMATS,
        choices=["txt", "srt", "vtt", "json", "tsv"],
        help="Output formats"
    )
    parser.add_argument(
        "--keep-audio",
        action="store_true",
        help="Keep downloaded audio files"
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Force CPU usage (disable GPU)"
    )
    
    args = parser.parse_args()
    
    # Determine device
    device = "cpu" if args.cpu else config.DEVICE
    
    # Initialize transcriber
    transcriber = YouTubeTranscriber(
        model_name=args.model,
        device=device,
        use_fp16=config.USE_FP16 and not args.cpu
    )
    
    # Process videos
    if len(args.url) == 1:
        result = transcriber.process_youtube_url(
            args.url[0],
            output_formats=args.output_formats,
            keep_audio=args.keep_audio
        )
        logger.info(f"Successfully processed: {result['video_title']}")
        logger.info(f"Output files: {result['output_files']}")
    else:
        results = transcriber.process_batch(
            args.url,
            output_formats=args.output_formats,
            keep_audio=args.keep_audio
        )
        successful = sum(1 for r in results if "error" not in r)
        logger.info(f"Processed {successful}/{len(results)} videos successfully")


if __name__ == "__main__":
    main()
