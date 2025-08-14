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

def generate_audio(text, voice, speed, output_format='mp3'):
    """Generates audio files from the provided text."""
    generator = pipeline(text, voice=voice, speed=speed, split_pattern=r'\n+')
    
    output_dir = 'tmp'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    audio_files = []
    for i, (_, _, audio) in enumerate(generator):
        file_path = f'{output_dir}/{i}.{output_format}'
        sf.write(file_path, audio, 24000)  # Save each segment to specified format
        audio_files.append(file_path)
    
    return audio_files

def merge_audio_files(audio_files, output_dir='outputs', output_format='mp3', custom_filename=None):
    """Merges multiple audio files into a single file."""
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Use custom filename or generate timestamp-based filename
    if custom_filename:
        filename = custom_filename
    else:
        filename = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
    
    merged_output_path = os.path.join(output_dir, f'{filename}.{output_format}')
    
    # Check if file already exists
    if os.path.exists(merged_output_path):
        print(f"Error: File '{merged_output_path}' already exists.")
        print("Please choose a different filename or remove the existing file.")
        sys.exit(1)
    
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
    # Set MPS environment variable if requested
    if args.mps:
        os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
        print("GPU acceleration (MPS) enabled.")
    
    if args.source:
        with open(args.source, 'r') as file:
            text = file.read()
    else:
        text = args.text

    print("Generating audio...")
    audio_files = generate_audio(text, args.voice, args.speed, args.format)

    print("Merging audio files...")
    merged_file = merge_audio_files(audio_files, args.output, args.format, args.filename)

    print(f"Audio output saved to {merged_file}")

    print("Cleaning up temporary files...")
    clean_up(audio_files)
    print("Process completed successfully.")

def main():
    import warnings    
    parser = argparse.ArgumentParser(description="CLI tool for offline text-to-speech")

    parser.add_argument('text', nargs='?', help="Raw text to synthesize.")
    parser.add_argument('-f', '--source', help="Path to a source document file (e.g., README.md).")
    parser.add_argument('-s', '--speed', type=float, default=1.0, help="Speed of the speech synthesis (default: 1.0).")
    parser.add_argument('-v', '--voice', default='af_heart', help="Voice to use for synthesis (default: af_heart).")
    parser.add_argument('--mps', action='store_true', help="Enable Mac OS MPS GPU acceleration.")
    parser.add_argument('--format', choices=['mp3', 'wav'], default='mp3', help="Output audio format (default: mp3).")
    parser.add_argument('-o', '--output', default='outputs', help="Output directory for generated audio files (default: outputs).")
    parser.add_argument('--filename', help="Custom filename for the output audio file (without extension).")

    args = parser.parse_args()

    # Ensure at least one input is provided
    if not args.text and not args.source:
        print("Error: Please provide either raw text or a source file path.")
        parser.print_help()
        sys.exit(1)

    # Process the input and generate audio
    with warnings.catch_warnings():
        process_input(args)

if __name__ == '__main__':
    main()