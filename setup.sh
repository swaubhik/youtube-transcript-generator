#!/bin/bash
# Setup script for YouTube Whisper Transcription
# For Ubuntu with NVIDIA GPU

set -e

echo "==========================================="
echo "YouTube Whisper Transcription Setup"
echo "==========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${YELLOW}Warning: This script is designed for Ubuntu/Linux${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for Python 3
echo -e "${GREEN}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed!${NC}"
    echo "Install it with: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found: $(python3 --version)${NC}"

# Check for FFmpeg
echo -e "\n${GREEN}Checking FFmpeg installation...${NC}"
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${YELLOW}FFmpeg not found. Installing...${NC}"
    sudo apt update
    sudo apt install ffmpeg -y
    echo -e "${GREEN}✓ FFmpeg installed${NC}"
else
    echo -e "${GREEN}✓ FFmpeg found: $(ffmpeg -version | head -n 1)${NC}"
fi

# Check for NVIDIA GPU
echo -e "\n${GREEN}Checking for NVIDIA GPU...${NC}"
if command -v nvidia-smi &> /dev/null; then
    echo -e "${GREEN}✓ NVIDIA GPU detected:${NC}"
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
else
    echo -e "${YELLOW}Warning: nvidia-smi not found. GPU acceleration may not be available.${NC}"
    echo -e "${YELLOW}Install NVIDIA drivers if you have a GPU.${NC}"
fi

# Create virtual environment
echo -e "\n${GREEN}Creating Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "\n${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "\n${GREEN}Upgrading pip...${NC}"
pip install --upgrade pip

# Install PyTorch with CUDA support
echo -e "\n${GREEN}Installing PyTorch with CUDA support...${NC}"
echo "This may take a few minutes..."
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other dependencies
echo -e "\n${GREEN}Installing other dependencies...${NC}"
pip install -U openai-whisper yt-dlp ffmpeg-python tqdm numpy

# Verify installation
echo -e "\n${GREEN}Verifying installation...${NC}"
python3 << EOF
import torch
import whisper
import yt_dlp

print(f"✓ PyTorch version: {torch.__version__}")
print(f"✓ CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"✓ CUDA version: {torch.version.cuda}")
    print(f"✓ GPU: {torch.cuda.get_device_name(0)}")
    print(f"✓ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
print(f"✓ Whisper installed")
print(f"✓ yt-dlp installed")
EOF

echo -e "\n${GREEN}==========================================="
echo "Setup completed successfully!"
echo "==========================================${NC}"
echo ""
echo "To use the transcription tool:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the transcription script:"
echo "     python main.py \"YOUR_YOUTUBE_URL\""
echo ""
echo "  3. See README.md for more usage examples"
echo ""
echo -e "${GREEN}Happy transcribing!${NC}"
