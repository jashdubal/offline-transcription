# offline proofreading
CLI tool to easily provide text-to-speech on raw text or documents. Uses [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) under the hood.

## Requirements
#### Install kokoro TTS model
```
pip install -q kokoro>=0.3.4 soundfile
```

#### Install espeak, used for English OOD fallback and some non-English languages (Linux/Windows)
```
apt-get -qq -y install espeak-ng > /dev/null 2>&1
```

## Usage
#### Raw text:
```
python3 cli.py "living the dream" -s 1 -v af_bella
```

#### Document:
```
python3 cli.py -f README.md -s 1 -v af_bella
```

#### Installing globally:
``` python
# Move to cli script to a global location
sudo cp cli.py /usr/local/bin/<NAME_OF_SCRIPT>

# Make script executable
chmod +x /usr/local/bin/<NAME_OF_SCRIPT>

# Run: <NAME_OF_SCRIPT> "living the dream" -s 1 -v af_bella
# OR: <NAME_OF_SCRIPT> -f test.txt -s 1 -v af_bella
```

For documentation on voices see [VOICES.md](VOICES.md)