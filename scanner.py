import os

SUPPORTED_EXTENSIONS = {'.mp3', '.flac', '.m4a', '.ogg', '.opus', '.wav'}

def scan_directory(path):
    """
    Generator that yields paths to supported audio files in the given directory.
    Recursively scans subdirectories.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in SUPPORTED_EXTENSIONS:
                yield os.path.join(root, file)
