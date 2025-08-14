# Offline TTS
CLI tool to generate text-to-speech for raw text or documents. Uses [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) under the hood.

## Requirements

> Having python3 installed.

### Using UV
UV is a modern python package and venv manager. You don't have to use it but if you do don't forgot to set it up properly:

```
uv init
source .venv/bin/activate && python -m ensurepip --upgrade
```

### Install kokoro TTS model

#### Using pip 

```
pip install -q kokoro>=0.3.4 soundfile
```

#### Using UV

```
uv add kokoro soundfile
```

### Install espeak, used for English OOD fallback and some non-English languages (Linux/Windows)

```
# Mac
brew install espeak-ng
# Linux
apt-get -qq -y install espeak-ng > /dev/null 2>&1
```

## Usage

### Using the executable script (recommended):
```bash
# Raw text with default settings
bin/tts "living the dream"

# Raw text with custom voice and speed
bin/tts "living the dream" -s 1.2 -v af_bella

# Document with GPU acceleration and custom output format
bin/tts -f README.md --mps --format wav -o my_audio

# Custom filename (will not overwrite existing files)
bin/tts "hello world" --filename "my_greeting"

# All options example
bin/tts "hello world" -s 0.8 -v af_heart --mps --format mp3 -o outputs --filename "custom_audio"
```

### Command line options:
- `--mps`: Enable Mac OS MPS GPU acceleration (replaces manual PYTORCH_ENABLE_MPS_FALLBACK=1)
- `--format`: Output format - mp3 (default) or wav
- `-o, --output`: Output directory (default: outputs)
- `--filename`: Custom filename for output (without extension). Will not overwrite existing files.
- `-s, --speed`: Speech speed (default: 1.0)
- `-v, --voice`: Voice to use (default: af_heart)
- `-f, --source`: Path to source document file instead of raw text

### Traditional usage (if not using the executable script):

```bash
# With python3
python3 cli.py "living the dream" -s 1 -v af_bella --mps
# With UV
uv run cli.py "living the dream" -s 1 -v af_bella --mps
# Source file example
uv run cli.py -f README.md --mps --format wav --filename "readme_audio"
```

On first run you will have to download the weights which will take some time:

```
kokoro-v1_0.pth: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 327M/327M [01:51<00:00, 2.94MB/s]
```

### Voices

For documentation on voices see [VOICES.md](VOICES.md)