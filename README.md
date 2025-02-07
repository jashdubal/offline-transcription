# offline proofreading
Implementation of CLI tool to easily provide text-to-speech on raw text or documents. [Uses hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) under the hood.

## Requirements
#### Install kokoro TTS model
`pip install -q kokoro>=0.3.4 soundfile`

#### Install espeak, used for English OOD fallback and some non-English languages (Linux/Windows)
`apt-get -qq -y install espeak-ng > /dev/null 2>&1`

## Usage
Raw text:
```
python3 cli.py "living the dream" -s 1 -v af_bella
```

Document:
```
python3 cli.py -f README.md -s 1 -v af_bella
```

## Voices
- (provided by hexgrad/Kokoro-82M)


| Name | Traits | Target Quality | Training Duration | Overall Grade | SHA256 |
| ---- | ------ | -------------- | ----------------- | ------------- | ------ |
| **af\_heart** | 🚺❤️ | | | **A** | `0ab5709b` |
| af_alloy | 🚺 | B | MM minutes | C | `6d877149` |
| af_aoede | 🚺 | B | H hours | C+ | `c03bd1a4` |
| af_bella | 🚺🔥 | **A** | **HH hours** | **A-** | `8cb64e02` |
| af_jessica | 🚺 | C | MM minutes | D | `cdfdccb8` |
| af_kore | 🚺 | B | H hours | C+ | `8bfbc512` |
| af_nicole | 🚺🎧 | B | **HH hours** | B- | `c5561808` |
| af_nova | 🚺 | B | MM minutes | C | `e0233676` |
| af_river | 🚺 | C | MM minutes | D | `e149459b` |
| af_sarah | 🚺 | B | H hours | C+ | `49bd364e` |
| af_sky | 🚺 | B | _M minutes_ 🤏 | C- | `c799548a` |
| am_adam | 🚹 | D | H hours | F+ | `ced7e284` |
| am_echo | 🚹 | C | MM minutes | D | `8bcfdc85` |
| am_eric | 🚹 | C | MM minutes | D | `ada66f0e` |
| am_fenrir | 🚹 | B | H hours | C+ | `98e507ec` |
| am_liam | 🚹 | C | MM minutes | D | `c8255075` |
| am_michael | 🚹 | B | H hours | C+ | `9a443b79` |
| am_onyx | 🚹 | C | MM minutes | D | `e8452be1` |
| am_puck | 🚹 | B | H hours | C+ | `dd1d8973` |
| am_santa | 🚹 | C | _M minutes_ 🤏 | D- | `7f2f7582` |