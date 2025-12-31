A Python CLI clone of lrcget for downloading lyrics from lrclib.net.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the scanner on your music directory:

```bash
python main.py /path/to/music
```

### Options

- `--force`: Overwrite existing .lrc files.
- `--verbose`: Show detailed output (skips, searches, etc.).
- `--help`: Show help message.

## Features

- Recursively scans for `.mp3`, `.flac`, `.m4a`, `.ogg`, `.opus`, `.wav`.
- Extracts metadata (Artist, Title, Album, Duration).
- Fetches synced lyrics from `lrclib.net`.
- Saves `.lrc` files next to audio files.
