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
from play import play_audio_file

pipeline = KPipeline(lang_code='a')

# Global variable for silent mode
SILENT_MODE = False

def log_info(message, emoji="ℹ️"):
    """Log informational messages with emoji, respecting silent mode."""
    if not SILENT_MODE:
        print(f"{emoji} {message}")

def log_success(message, emoji="✅"):
    """Log success messages with emoji, respecting silent mode."""
    if not SILENT_MODE:
        print(f"{emoji} {message}")

def log_error(message, emoji="❌"):
    """Log error messages with emoji (always shown)."""
    print(f"{emoji} {message}")

def log_progress(message, emoji="⏳"):
    """Log progress messages with emoji, respecting silent mode."""
    if not SILENT_MODE:
        print(f"{emoji} {message}")


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
        log_error(f"File '{merged_output_path}' already exists.")
        log_error("Please choose a different filename or remove the existing file.")
        sys.exit(1)
    
    merged_audio = []

    for file in audio_files:
        audio_data, samplerate = sf.read(file)
        merged_audio.extend(audio_data)
    sf.write(merged_output_path, merged_audio, 24000)
    return merged_output_path

def merge_audio_files_temp(audio_files, output_format='mp3'):
    """Merges multiple audio files into a single temporary file for preview."""
    # Create temporary merged file
    temp_filename = f'tmp/preview.{output_format}'
    merged_audio = []

    for file in audio_files:
        audio_data, samplerate = sf.read(file)
        merged_audio.extend(audio_data)
    sf.write(temp_filename, merged_audio, 24000)
    return temp_filename

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
        log_info("GPU acceleration (MPS) enabled", "🚀")
    
    if args.source:
        with open(args.source, 'r') as file:
            text = file.read()
        log_info(f"Loaded text from: {args.source}", "📄")
    else:
        text = args.text

    log_progress("Generating audio segments...", "🎵")
    audio_files = generate_audio(text, args.voice, args.speed, args.format)

    if args.play_only:
        # Play-only mode: merge to temporary file, play, then clean up everything
        log_progress("Merging audio for preview...", "🔄")
        merged_file = merge_audio_files_temp(audio_files, args.format)
        
        log_progress("Playing audio preview...", "🔊")
        play_audio_file(merged_file, args.silent)
        
        log_progress("Cleaning up temporary files...", "🧹")
        clean_up(audio_files + [merged_file])  # Clean up segments + merged preview
        log_success("Preview completed successfully!", "🎉")
    else:
        # Normal mode: save to output directory
        log_progress("Merging audio files...", "🔄")
        merged_file = merge_audio_files(audio_files, args.output, args.format, args.filename)

        log_success(f"Audio saved: {os.path.basename(merged_file)}", "💾")

        # Play the audio file if requested
        if args.play:
            log_progress("Playing generated audio...", "🔊")
            play_audio_file(merged_file, args.silent)

        log_progress("Cleaning up temporary files...", "🧹")
        clean_up(audio_files)
        log_success("Process completed successfully!", "🎉")

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
    parser.add_argument('--play', action='store_true', help="Automatically play the generated audio file after creation.")
    parser.add_argument('--play-only', action='store_true', help="Generate and play audio without saving to output directory (temporary preview).")
    parser.add_argument('--silent', action='store_true', help="Silent mode - suppress all output except errors.")

    args = parser.parse_args()

    # Set silent mode globally
    global SILENT_MODE
    SILENT_MODE = args.silent
    
    # Ensure at least one input is provided
    if not args.text and not args.source:
        log_error("Please provide either raw text or a source file path.")
        if not args.silent:
            parser.print_help()
        sys.exit(1)

    # Process the input and generate audio
    with warnings.catch_warnings():
        process_input(args)

if __name__ == '__main__':
    main()