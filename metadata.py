import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
import os

def get_metadata(file_path):
    """
    Extracts metadata from an audio file.
    Returns a dict with: title, artist, album, duration (in seconds)
    """
    try:
        # Generic handling first for duration and basic tags
        audio = mutagen.File(file_path)
        if not audio:
            return None

        metadata = {
            "title": None,
            "artist": None,
            "album": None,
            "duration": audio.info.length if audio.info else 0
        }

        # Format specific extraction for better tag reliability
        if file_path.lower().endswith(".mp3"):
            # EasyID3 is simpler for standard tags
            try:
                tags = EasyID3(file_path)
                metadata["title"] = tags.get("title", [None])[0]
                metadata["artist"] = tags.get("artist", [None])[0]
                metadata["album"] = tags.get("album", [None])[0]
            except mutagen.id3.ID3NoHeaderError:
                pass 
        elif file_path.lower().endswith(".flac"):
            if isinstance(audio, FLAC):
                metadata["title"] = audio.get("title", [None])[0]
                metadata["artist"] = audio.get("artist", [None])[0]
                metadata["album"] = audio.get("album", [None])[0]
        elif file_path.lower().endswith(".m4a"):
            if isinstance(audio, MP4):
                # M4A tags are usually: \xa9nam (title), \xa9ART (artist), \xa9alb (album)
                metadata["title"] = audio.get("\xa9nam", [None])[0]
                metadata["artist"] = audio.get("\xa9ART", [None])[0]
                metadata["album"] = audio.get("\xa9alb", [None])[0]
        elif file_path.lower().endswith(".ogg"):
             if isinstance(audio, OggVorbis):
                metadata["title"] = audio.get("title", [None])[0]
                metadata["artist"] = audio.get("artist", [None])[0]
                metadata["album"] = audio.get("album", [None])[0]
        else:
            # Fallback for other formats supported by mutagen.File
            # This handles generic Ogg, Opus, etc. if they use standard keys
            tags = audio.tags
            if tags:
                metadata["title"] = tags.get("title", [None])[0]
                metadata["artist"] = tags.get("artist", [None])[0]
                metadata["album"] = tags.get("album", [None])[0]

        # Fallback: if title is missing, use filename without extension
        if not metadata["title"]:
            metadata["title"] = os.path.splitext(os.path.basename(file_path))[0]

        return metadata

    except Exception as e:
        # print(f"Error reading metadata for {file_path}: {e}")
        return None
