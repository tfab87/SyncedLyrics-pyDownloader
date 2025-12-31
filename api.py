import requests

BASE_URL = "https://lrclib.net"
USER_AGENT = "LRCGET-Python-Clone/0.1.0 (https://github.com/tranxuanthang/lrcget)"

def get_lyrics(title, artist, album, duration):
    """
    Fetches lyrics from lrclib.net.
    """
    params = {
        "track_name": title,
        "artist_name": artist,
        "album_name": album,
        "duration": str(round(duration)) if duration else "0"
    }
    
    # Filter out None values to avoid sending "None" strings
    params = {k: v for k, v in params.items() if v is not None}

    try:
        response = requests.get(
            f"{BASE_URL}/api/get",
            params=params,
            headers={"User-Agent": USER_AGENT},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            # print(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        # print(f"Request Error: {e}")
        return None
