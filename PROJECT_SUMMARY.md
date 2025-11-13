# YouTube Whisper Transcription - Project Complete! 🎉

Your workspace for transcribing YouTube videos using OpenAI Whisper is now ready!

## ✅ What's Been Created

### Core Files

- **main.py** - Main transcription script with CLI interface
- **config.py** - Configuration settings for GPU, models, and outputs
- **requirements.txt** - Python dependencies with CUDA support
- **setup.sh** - Automated setup script for Ubuntu

### Utilities (src/utils/)

- **logger.py** - Logging configuration
- **video_processor.py** - YouTube download utilities
- **file_handler.py** - Transcript saving in multiple formats

### Documentation

- **README.md** - Comprehensive documentation
- **QUICKSTART.md** - Quick reference guide
- **example.py** - Usage examples and code samples

### Project Structure

```
youtube/
├── .github/copilot-instructions.md  # GitHub Copilot guidance
├── .gitignore                        # Git ignore rules
├── config.py                         # Configuration
├── main.py                          # Main script
├── requirements.txt                 # Dependencies
├── setup.sh                         # Setup script
├── example.py                       # Examples
├── README.md                        # Full docs
├── QUICKSTART.md                    # Quick guide
├── src/
│   └── utils/
│       ├── logger.py
│       ├── video_processor.py
│       └── file_handler.py
├── downloads/                       # Temp audio files
└── outputs/                         # Transcription outputs
```

## 🚀 Next Steps

### 1. On Your Ubuntu Workstation

```bash
# Navigate to project
cd youtube

# Make setup script executable
chmod +x setup.sh

# Run setup (installs dependencies)
./setup.sh

# Activate virtual environment
source venv/bin/activate
```

### 2. Test Your Setup

```bash
# Verify GPU is detected
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Test with a short video
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --model base
```

### 3. Start Transcribing

```bash
# Use the best model (recommended for A6000)
python main.py "YOUR_VIDEO_URL" --model large-v3

# With all output formats
python main.py "YOUR_VIDEO_URL" --output-formats txt srt vtt json
```

## 🎯 Key Features

✅ **GPU Accelerated** - Optimized for NVIDIA A6000 (48GB VRAM)  
✅ **High Accuracy** - Uses latest Whisper large-v3 model  
✅ **Fast Processing** - FP16 precision for 2x speedup  
✅ **Multiple Formats** - TXT, SRT, VTT, JSON, TSV outputs  
✅ **Batch Processing** - Handle multiple videos at once  
✅ **Auto Language Detection** - Supports 90+ languages  
✅ **Easy to Use** - Simple CLI and Python API

## 📊 Performance on A6000

| Model    | Speed (approx.) | VRAM Usage |
| -------- | --------------- | ---------- |
| tiny     | 100x realtime   | ~1 GB      |
| base     | 50x realtime    | ~1 GB      |
| small    | 20x realtime    | ~2 GB      |
| medium   | 8x realtime     | ~5 GB      |
| large-v3 | 4x realtime     | ~10 GB     |

\*With FP16 enabled on A6000

## 💡 Pro Tips

1. **First run** will download the model (~3GB for large-v3)
2. **Keep audio files** with `--keep-audio` flag for debugging
3. **Monitor GPU** with `watch -n 1 nvidia-smi`
4. **Use large-v3** - Your A6000 can handle it easily!
5. **Batch processing** - Process playlists overnight

## 📚 Documentation

- **Full Guide**: See `README.md`
- **Quick Reference**: See `QUICKSTART.md`
- **Code Examples**: See `example.py`
- **Configuration**: See `config.py`

## 🔧 Customization

Edit `config.py` to change:

- Default Whisper model
- GPU settings (FP16, device)
- Output formats
- Language settings
- Logging level

## 🐛 Troubleshooting

If you encounter issues:

1. Check `README.md` troubleshooting section
2. Verify NVIDIA drivers: `nvidia-smi`
3. Verify CUDA: `python -c "import torch; print(torch.cuda.is_available())"`
4. Update yt-dlp: `pip install -U yt-dlp`

## 🎓 Learning Resources

- [OpenAI Whisper Docs](https://github.com/openai/whisper)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [PyTorch CUDA Guide](https://pytorch.org/get-started/locally/)

---

**Ready to transcribe? Start with QUICKSTART.md!** 🚀
