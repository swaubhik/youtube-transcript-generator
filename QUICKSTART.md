# Quick Start Guide

## Installation (Ubuntu with NVIDIA GPU)

```bash
# 1. Make setup script executable
chmod +x setup.sh

# 2. Run setup script
./setup.sh

# 3. Activate virtual environment
source venv/bin/activate
```

## Basic Usage

### Single Video

```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### With Options

```bash
# Large model (best quality)
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --model large-v3

# Specific language
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --language en

# Multiple formats
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --output-formats txt srt vtt json

# Keep audio file
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --keep-audio
```

### Multiple Videos

```bash
python main.py \
  "https://www.youtube.com/watch?v=VIDEO_ID_1" \
  "https://www.youtube.com/watch?v=VIDEO_ID_2" \
  --model large-v3
```

## Model Selection Guide

| Use Case          | Model    | Speed     | Accuracy  |
| ----------------- | -------- | --------- | --------- |
| Quick testing     | tiny     | Fastest   | Good      |
| Draft transcripts | base     | Very fast | Better    |
| General use       | small    | Fast      | Great     |
| High accuracy     | medium   | Moderate  | Excellent |
| Best quality      | large-v3 | Slowest   | Best      |

**Recommendation for A6000**: Use `large-v3` for best results

## Output Files

Files are saved to `outputs/` directory:

- `VIDEO_ID_TITLE.txt` - Plain text
- `VIDEO_ID_TITLE.srt` - Subtitles (video players)
- `VIDEO_ID_TITLE.vtt` - Web subtitles
- `VIDEO_ID_TITLE.json` - Full data with timestamps

## Common Commands

```bash
# Check GPU status
nvidia-smi

# Monitor GPU during transcription
watch -n 1 nvidia-smi

# Verify CUDA is working
python -c "import torch; print(torch.cuda.is_available())"

# Clean downloaded audio files
rm downloads/*

# View logs with INFO level
# (default, shows progress)

# Activate environment (run before each session)
source venv/bin/activate
```

## Troubleshooting

### GPU not detected

```bash
# Check NVIDIA driver
nvidia-smi

# Reinstall PyTorch with CUDA
pip uninstall torch torchaudio
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Out of memory

```bash
# Use smaller model
python main.py URL --model medium

# Or force CPU
python main.py URL --cpu
```

### FFmpeg errors

```bash
# Reinstall FFmpeg
sudo apt install --reinstall ffmpeg
```

## Tips

1. **First run**: Downloads model (~3GB for large-v3)
2. **Speed**: FP16 on GPU is ~2x faster than FP32
3. **Accuracy**: English works best; other languages supported
4. **Batch**: Process multiple videos overnight
5. **Storage**: Keep `downloads/` clean to save space

## Need Help?

- See `README.md` for full documentation
- Check `example.py` for code examples
- Review `config.py` for customization options
