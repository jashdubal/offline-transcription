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

> On Mac OS use the PYTORCH_ENABLE_MPS_FALLBACK=1 flag to use GPU acceleration

### Raw text:
```
# With python3
PYTORCH_ENABLE_MPS_FALLBACK=1 python3 cli.py "living the dream" -s 1 -v af_bella
# With UV
PYTORCH_ENABLE_MPS_FALLBACK=1 uv run cli.py "living the dream" -s 1 -v af_bella
```

### Document:
```
# With python3
PYTORCH_ENABLE_MPS_FALLBACK=1 python3 cli.py -f README.md -s 1 -v af_bella
# With UV
PYTORCH_ENABLE_MPS_FALLBACK=1 uv run cli.py -f README.md -s 1 -v af_bella
```

On first run you will have to download the weights which will take some time:

```
kokoro-v1_0.pth: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 327M/327M [01:51<00:00, 2.94MB/s]
```

### Voices

For documentation on voices see [VOICES.md](VOICES.md)