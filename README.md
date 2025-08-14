# Offline TTS
CLI tool to generate text-to-speech for raw text or documents. Uses [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) under the hood.

- [Offline TTS](#offline-tts)
  - [Requirements](#requirements)
    - [Using UV](#using-uv)
    - [Install kokoro TTS model](#install-kokoro-tts-model)
      - [Using pip](#using-pip)
      - [Using UV](#using-uv-1)
    - [Install espeak, used for English OOD fallback and some non-English languages (Linux/Windows)](#install-espeak-used-for-english-ood-fallback-and-some-non-english-languages-linuxwindows)
  - [Usage](#usage)
    - [Using the executable script (recommended):](#using-the-executable-script-recommended)
    - [Command line options:](#command-line-options)
    - [Traditional usage (if not using the executable script):](#traditional-usage-if-not-using-the-executable-script)
  - [Audio Playback](#audio-playback)
    - [Using the audio player:](#using-the-audio-player)
    - [Audio player options:](#audio-player-options)
    - [Voices](#voices)


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

# Play audio immediately after generation (uses integrated player)
bin/tts "hello world" --play

# Generate audio and play later with standalone player
bin/tts "hello world" --filename "my_audio"
bin/play --latest

# All options example
bin/tts "hello world" -s 0.8 -v af_heart --mps --format mp3 -o outputs --filename "custom_audio" --play
```

### Command line options:
- `--mps`: Enable Mac OS MPS GPU acceleration (replaces manual PYTORCH_ENABLE_MPS_FALLBACK=1)
- `--format`: Output format - mp3 (default) or wav
- `-o, --output`: Output directory (default: outputs)
- `--filename`: Custom filename for output (without extension). Will not overwrite existing files.
- `--play`: Automatically play the generated audio file after creation (supports macOS, Linux, Windows)
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

## Audio Playback

The project includes a standalone audio player for playing generated TTS files or any other audio files.

### Using the audio player:

```bash
# Play a specific audio file
bin/play path/to/audio.mp3

# Play the latest generated audio file
bin/play --latest

# List all audio files in the outputs directory
bin/play --list -d outputs

# Play all audio files in a directory
bin/play -d outputs

# Verbose output
bin/play --latest -v
```

### Audio player options:
- `file`: Path to specific audio file to play
- `-d, --directory`: Play all audio files in a directory
- `-l, --list`: List audio files in current or specified directory  
- `--latest`: Play the most recently created audio file in outputs directory
- `-v, --verbose`: Show detailed output during playback

### Voices

For documentation on voices see [VOICES.md](VOICES.md)