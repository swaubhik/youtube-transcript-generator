"""
Example usage scripts for YouTube Whisper transcription
"""
from main import YouTubeTranscriber
import config


def example_single_video():
    """Example: Transcribe a single video"""
    print("Example 1: Transcribing a single video\n")
    
    # Initialize transcriber with large-v3 model
    transcriber = YouTubeTranscriber(
        model_name="large-v3",
        device="cuda",
        use_fp16=True
    )
    
    # Transcribe a video
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with your video URL
    
    result = transcriber.process_youtube_url(
        url,
        output_formats=["txt", "srt", "json"],
        keep_audio=False
    )
    
    print(f"✓ Transcribed: {result['video_title']}")
    print(f"✓ Language: {result['language']}")
    print(f"✓ Output files:")
    for fmt, path in result['output_files'].items():
        print(f"  - {fmt.upper()}: {path}")


def example_batch_processing():
    """Example: Process multiple videos"""
    print("\nExample 2: Batch processing multiple videos\n")
    
    # Initialize with a smaller model for faster processing
    transcriber = YouTubeTranscriber(
        model_name="medium",
        device="cuda",
        use_fp16=True
    )
    
    # List of video URLs to process
    urls = [
        "https://www.youtube.com/watch?v=VIDEO_ID_1",
        "https://www.youtube.com/watch?v=VIDEO_ID_2",
        "https://www.youtube.com/watch?v=VIDEO_ID_3",
    ]
    
    results = transcriber.process_batch(
        urls,
        output_formats=["txt", "srt"],
        keep_audio=False
    )
    
    # Print summary
    successful = sum(1 for r in results if "error" not in r)
    print(f"\n✓ Successfully processed {successful}/{len(results)} videos")
    
    for i, result in enumerate(results, 1):
        if "error" not in result:
            print(f"{i}. {result['video_title']} ({result['language']})")
        else:
            print(f"{i}. Error: {result['error']}")


def example_with_specific_language():
    """Example: Transcribe with specific language setting"""
    print("\nExample 3: Transcribe with specific language\n")
    
    transcriber = YouTubeTranscriber(model_name="large-v3")
    
    # Override config for this specific transcription
    url = "https://www.youtube.com/watch?v=VIDEO_ID"
    
    # Manually transcribe with language specification
    import os
    from src.utils.video_processor import download_audio, get_video_info
    from src.utils.file_handler import save_transcript
    
    video_info = get_video_info(url)
    audio_path = download_audio(url, config.DOWNLOADS_DIR)
    
    # Transcribe with Spanish language
    result = transcriber.transcribe_audio(
        audio_path,
        language="es",  # Spanish
        task="transcribe"
    )
    
    # Save outputs
    output_files = save_transcript(
        result,
        video_info['id'],
        video_info['title'],
        config.OUTPUTS_DIR,
        ["txt", "srt"]
    )
    
    print(f"✓ Transcribed in Spanish: {video_info['title']}")
    print(f"✓ Outputs: {output_files}")
    
    # Cleanup
    if not config.KEEP_AUDIO:
        os.remove(audio_path)


def example_translate_to_english():
    """Example: Translate non-English video to English"""
    print("\nExample 4: Translate to English\n")
    
    transcriber = YouTubeTranscriber(model_name="large-v3")
    
    url = "https://www.youtube.com/watch?v=VIDEO_ID"  # Non-English video
    
    import os
    from src.utils.video_processor import download_audio, get_video_info
    from src.utils.file_handler import save_transcript
    
    video_info = get_video_info(url)
    audio_path = download_audio(url, config.DOWNLOADS_DIR)
    
    # Translate to English
    result = transcriber.transcribe_audio(
        audio_path,
        task="translate"  # This translates to English
    )
    
    output_files = save_transcript(
        result,
        video_info['id'],
        video_info['title'] + "_EN",
        config.OUTPUTS_DIR,
        ["txt", "srt"]
    )
    
    print(f"✓ Translated to English: {video_info['title']}")
    print(f"✓ Outputs: {output_files}")
    
    # Cleanup
    os.remove(audio_path)


def example_cpu_mode():
    """Example: Run on CPU instead of GPU"""
    print("\nExample 5: CPU-only mode\n")
    
    # Initialize with CPU
    transcriber = YouTubeTranscriber(
        model_name="base",  # Use smaller model for CPU
        device="cpu",
        use_fp16=False  # FP16 not supported on CPU
    )
    
    url = "https://www.youtube.com/watch?v=VIDEO_ID"
    
    result = transcriber.process_youtube_url(url, output_formats=["txt"])
    
    print(f"✓ Transcribed on CPU: {result['video_title']}")


def example_custom_output_directory():
    """Example: Save outputs to custom directory"""
    print("\nExample 6: Custom output directory\n")
    
    from pathlib import Path
    import os
    from src.utils.video_processor import download_audio, get_video_info
    from src.utils.file_handler import save_transcript
    
    transcriber = YouTubeTranscriber(model_name="medium")
    
    url = "https://www.youtube.com/watch?v=VIDEO_ID"
    custom_output_dir = Path("./my_transcripts")
    custom_output_dir.mkdir(exist_ok=True)
    
    video_info = get_video_info(url)
    audio_path = download_audio(url, config.DOWNLOADS_DIR)
    result = transcriber.transcribe_audio(audio_path)
    
    output_files = save_transcript(
        result,
        video_info['id'],
        video_info['title'],
        custom_output_dir,
        ["txt", "srt", "vtt", "json"]
    )
    
    print(f"✓ Saved to custom directory: {custom_output_dir}")
    print(f"✓ Files: {output_files}")
    
    os.remove(audio_path)


if __name__ == "__main__":
    print("=" * 70)
    print("YouTube Whisper Transcription - Usage Examples")
    print("=" * 70)
    
    print("\nNOTE: Replace VIDEO_ID placeholders with actual YouTube video IDs")
    print("      before running these examples.\n")
    
    # Uncomment the example you want to run:
    
    # example_single_video()
    # example_batch_processing()
    # example_with_specific_language()
    # example_translate_to_english()
    # example_cpu_mode()
    # example_custom_output_directory()
    
    print("\n" + "=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)
