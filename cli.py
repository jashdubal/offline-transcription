#!/usr/bin/env python3
import warnings
warnings.filterwarnings("ignore")

import argparse
import os
import sys
import shutil
from datetime import datetime
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')

def generate_audio(text, voice, speed):
    """Generates audio files from the provided text."""
    generator = pipeline(text, voice=voice, speed=speed, split_pattern=r'\n+')
    
    output_dir = 'tmp'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    audio_files = []
    for i, (_, _, audio) in enumerate(generator):
        file_path = f'{output_dir}/{i}.mp3'
        sf.write(file_path, audio, 24000)  # Save each segment to a .mp3 file
        audio_files.append(file_path)
    
    return audio_files

def merge_audio_files(audio_files):
    """Merges multiple audio files into a single file."""
    merged_output_path = datetime.now().strftime('%y-%m-%d-%H-%M-%S.mp3')
    merged_audio = []

    for file in audio_files:
        audio_data, samplerate = sf.read(file)
        merged_audio.extend(audio_data)
    sf.write(merged_output_path, merged_audio, 24000)
    return merged_output_path

def clean_up(files):
    """Deletes temporary audio files."""
    for file in files:
        os.remove(file)
    if os.path.exists('tmp'):
        shutil.rmtree('tmp')

def process_input(args):
    """Handles the CLI input and generates the TTS output."""
    if args.file:
        with open(args.file, 'r') as file:
            text = file.read()
    else:
        text = args.text

    print("Generating audio...")
    audio_files = generate_audio(text, args.voice, args.speed)

    print("Merging audio files...")
    merged_file = merge_audio_files(audio_files)

    print(f"Audio output saved to {merged_file}")

    print("Cleaning up temporary files...")
    clean_up(audio_files)
    print("Process completed successfully.")

def main():
    import warnings    
    parser = argparse.ArgumentParser(description="CLI tool for offline text-to-speech")

    parser.add_argument('text', nargs='?', help="Raw text to synthesize.")
    parser.add_argument('-f', '--file', help="Path to a document file (e.g., README.md).")
    parser.add_argument('-s', '--speed', type=float, default=1.0, help="Speed of the speech synthesis (default: 1.0).")
    parser.add_argument('-v', '--voice', default='af_heart', help="Voice to use for synthesis (default: af_heart).")

    args = parser.parse_args()

    # Ensure at least one input is provided
    if not args.text and not args.file:
        print("Error: Please provide either raw text or a file path.")
        parser.print_help()
        sys.exit(1)

    # Process the input and generate audio
    with warnings.catch_warnings():
        process_input(args)

if __name__ == '__main__':
    main()