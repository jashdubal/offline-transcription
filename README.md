# offline proofreading
Implementation of CLI tool to easily provide text-to-speech on raw text or documents. Uses hexgrad/Kokoro-82M[https://huggingface.co/hexgrad/Kokoro-82M] under the hood.

## Usage

Document:
```
proofo README.md -s 1 -v af_bella
```

Raw text:
```
proofo "living the dream" -s 1 -v af_bella
```
