# YouTube Whisper Transcription

A Python tool for transcribing YouTube videos using OpenAI Whisper with GPU acceleration. Optimized for NVIDIA A6000 GPUs running on Ubuntu.

## Features

- 🎥 Download audio from YouTube videos using yt-dlp
- 🎯 High-accuracy transcription using OpenAI Whisper
- 🚀 GPU acceleration with CUDA support (optimized for NVIDIA A6000)
- 📝 Multiple output formats: TXT, SRT, VTT, JSON, TSV
- 🌍 Multi-language support with auto-detection
- 📦 Batch processing for multiple videos
- ⚡ FP16 precision for faster inference
- 🔧 Configurable model sizes (tiny to large-v3)
- 📊 Real-time progress bars for download and transcription

## System Requirements

### Hardware

- **GPU**: NVIDIA A6000 (or any CUDA-compatible GPU)
- **RAM**: 16GB+ recommended
- **Storage**: Depends on model size and number of videos

### Software

- **OS**: Ubuntu 20.04+ (or any Linux distribution)
- **Python**: 3.8 or higher
- **CUDA**: 11.8 or higher
- **FFmpeg**: Required for audio processing

## Installation

### 1. Install System Dependencies

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install FFmpeg
sudo apt install ffmpeg -y

# Verify FFmpeg installation
ffmpeg -version
```

### 2. Install NVIDIA Drivers and CUDA (if not already installed)

```bash
# Check if NVIDIA driver is installed
nvidia-smi

# If not installed, install NVIDIA drivers
sudo apt install nvidia-driver-525 -y

# Install CUDA Toolkit (if needed)
# Follow instructions at: https://developer.nvidia.com/cuda-downloads
```

### 3. Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 4. Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install PyTorch with CUDA support (adjust CUDA version if needed)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other dependencies
pip install -U openai-whisper yt-dlp ffmpeg-python tqdm numpy

# Or install all from requirements.txt
pip install -r requirements.txt
```

### 5. Verify GPU Support

```python
# Run this Python script to verify GPU is accessible
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
```

## Usage

### Basic Usage

Transcribe a single YouTube video:

```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Advanced Options

```bash
# Use a specific model (tiny, base, small, medium, large-v2, large-v3)
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --model large-v3

# Specify language (auto-detect if not specified)
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --language en

# Translate to English instead of transcribing
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --task translate

# Choose output formats
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --output-formats txt srt json

# Keep downloaded audio files
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --keep-audio

# Force CPU usage (disable GPU)
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --cpu
```

### Batch Processing

Transcribe multiple videos:

```bash
python main.py \
  "https://www.youtube.com/watch?v=VIDEO_ID_1" \
  "https://www.youtube.com/watch?v=VIDEO_ID_2" \
  "https://www.youtube.com/watch?v=VIDEO_ID_3" \
  --model large-v3
```

### Python API Usage

```python
from main import YouTubeTranscriber

# Initialize transcriber
transcriber = YouTubeTranscriber(
    model_name="large-v3",
    device="cuda",
    use_fp16=True
)

# Transcribe a single video
result = transcriber.process_youtube_url(
    "https://www.youtube.com/watch?v=VIDEO_ID",
    output_formats=["txt", "srt", "json"],
    keep_audio=False
)

print(f"Title: {result['video_title']}")
print(f"Language: {result['language']}")
print(f"Output files: {result['output_files']}")

# Batch processing
urls = [
    "https://www.youtube.com/watch?v=VIDEO_ID_1",
    "https://www.youtube.com/watch?v=VIDEO_ID_2",
]
results = transcriber.process_batch(urls)
```

## Configuration

Edit `config.py` to customize default settings:

```python
# Whisper model (tiny, base, small, medium, large-v2, large-v3)
WHISPER_MODEL = "large-v3"

# GPU settings
USE_GPU = True
USE_FP16 = True  # Faster on GPU, slightly less accurate

# Language and task
LANGUAGE = None  # Auto-detect, or set to 'en', 'es', etc.
TASK = "transcribe"  # or "translate"

# Output formats
OUTPUT_FORMATS = ["txt", "srt", "vtt", "json"]

# Logging
LOG_LEVEL = "INFO"
```

## Whisper Model Comparison

| Model    | Parameters | VRAM Usage | Speed (relative) | Accuracy  |
| -------- | ---------- | ---------- | ---------------- | --------- |
| tiny     | 39 M       | ~1 GB      | ~32x             | Good      |
| base     | 74 M       | ~1 GB      | ~16x             | Better    |
| small    | 244 M      | ~2 GB      | ~6x              | Great     |
| medium   | 769 M      | ~5 GB      | ~2x              | Excellent |
| large-v2 | 1550 M     | ~10 GB     | 1x               | Best      |
| large-v3 | 1550 M     | ~10 GB     | 1x               | Best      |

**Note**: With an NVIDIA A6000 (48GB VRAM), you can comfortably use the largest models.

## Output Formats

- **TXT**: Plain text transcript
- **SRT**: SubRip subtitle format (for video players)
- **VTT**: WebVTT subtitle format (for web players)
- **JSON**: Full transcription data with timestamps and metadata
- **TSV**: Tab-separated values with timestamps

## Project Structure

```
youtube/
├── src/
│   ├── __init__.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Logging utilities
│       ├── video_processor.py  # YouTube download utilities
│       └── file_handler.py     # Transcript saving utilities
├── downloads/                  # Temporary audio files
├── outputs/                    # Transcription outputs
├── config.py                   # Configuration settings
├── main.py                     # Main script
├── example.py                  # Usage examples
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Troubleshooting

### CUDA Out of Memory

If you encounter GPU memory errors:

```bash
# Use a smaller model
python main.py URL --model medium

# Or disable FP16
# Edit config.py and set USE_FP16 = False
```

### FFmpeg Not Found

```bash
# Install FFmpeg
sudo apt install ffmpeg -y

# Verify installation
which ffmpeg
```

### yt-dlp Download Errors

```bash
# Update yt-dlp to the latest version
pip install -U yt-dlp
```

### Slow Transcription

- Ensure GPU is being used (check with `nvidia-smi`)
- Use FP16 precision (`USE_FP16 = True`)
- Use a smaller model for faster processing

## Performance Tips

1. **Use FP16 precision** for 2x speedup on modern GPUs
2. **Choose the right model**: Balance between speed and accuracy
3. **Batch processing**: Process multiple videos in sequence
4. **Monitor GPU usage**: Use `nvidia-smi` or `watch -n 1 nvidia-smi`

## GPU Monitoring

Monitor GPU usage during transcription:

```bash
# Real-time GPU monitoring
watch -n 1 nvidia-smi

# Or use
nvidia-smi dmon
```

## License

This project uses:

- OpenAI Whisper (MIT License)
- yt-dlp (Unlicense)
- PyTorch (BSD License)

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for the amazing speech recognition model
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube downloading capabilities
- [PyTorch](https://pytorch.org/) for GPU acceleration

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the [Whisper documentation](https://github.com/openai/whisper)
3. Create an issue in this repository
