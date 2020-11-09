import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Audio_Analyzer:
    def __init__(self):
        self._spotifyHandler = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials()
        )

        return
