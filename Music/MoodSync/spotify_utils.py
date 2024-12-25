import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Setup Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id="c7fa9d014d484456b7343e6b1c026187", client_secret="e15021f075c140969bd18244d967d6c0")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_spotify_track_id(song_name):
    results = sp.search(q=song_name, limit=1, type='track')
    if results['tracks']['items']:
        return results['tracks']['items'][0]['id']
    return None

def get_spotify_url(track_id):
    return f"https://open.spotify.com/track/{track_id}"
