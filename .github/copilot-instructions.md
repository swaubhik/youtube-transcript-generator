# YouTube Whisper Transcription Project

This is a Python project for transcribing YouTube videos using OpenAI Whisper with GPU acceleration.

## Project Status

- [x] Create .github/copilot-instructions.md
- [x] Get project setup information
- [x] Create project structure
- [x] Create requirements.txt with GPU support
- [x] Create main transcription script
- [x] Create configuration file
- [x] Create utility modules
- [x] Create README.md
- [x] Create example usage script

## Technical Stack

- Python 3.8+
- OpenAI Whisper for transcription
- yt-dlp for YouTube video downloading
- PyTorch with CUDA support for NVIDIA A6000 GPU
- FFmpeg for audio processing

## GPU Optimization

- Target hardware: NVIDIA A6000 (48GB VRAM)
- CUDA support enabled
- Optimized for large model inference (large-v2, large-v3)

## Code Style Guidelines

- Follow PEP 8 style guide
- Use type hints where appropriate
- Include docstrings for functions and classes
- Implement proper error handling and logging
