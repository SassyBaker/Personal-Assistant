import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()


def spotify_get_access_token():
    # Get token section
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    # Send HTTP to get token. Expires in 1 hour (3600s)
    response = requests.post(
        url="https://accounts.spotify.com/api/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
    )

    print(response.json())

    access_token = response.json()['access_token']

    return access_token


# Search for song
def spotify_search_for_song(song_name, session_key):
    result = requests.get(
        url="https://api.spotify.com/v1/search",
        headers={"Authorization": "Bearer " + session_key},
        params={
            "q": song_name,
            "type": "track",
            "limit": 1  # Number of results to return currently most played in spotify
        })

    # Select first result
    first_track = result.json()['tracks']['items'][0]
    track_name = first_track['name']
    track_artist = first_track['artists'][0]['name']
    spotify_track_id = first_track['id']

    return track_name, track_artist, spotify_track_id


def spotify_play_new_song(song_name):
    device_id = os.getenv('SPOTIFY_DEVICE_ID')
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    session_key = spotify_get_access_token()

    track_name, track_artist, spotify_track_id = spotify_search_for_song(song_name, session_key)

    # Play song
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri="http://localhost:8080",
                                                   scope="user-read-playback-state,user-modify-playback-state"))

    sp.start_playback(device_id=device_id, uris=[f'spotify:track:{spotify_track_id}'])

    return f"Playing '{track_name}' by '{track_artist}'"


def spotify_pause_song():
    device_id = os.getenv('SPOTIFY_DEVICE_ID')
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    # Play song
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri="http://localhost:8080",
                                                   scope="user-read-playback-state,user-modify-playback-state"))

    sp.pause_playback(device_id=device_id)



def spotify_resume_song():
    device_id = os.getenv('SPOTIFY_DEVICE_ID')
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    # Play song
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri="http://localhost:8080",
                                                   scope="user-read-playback-state,user-modify-playback-state"))

    sp.start_playback(device_id=device_id)


if __name__ == '__main__':
    # print(spotify_play_new_song("Clear My Head"))
    # spotify_pause_song()
    # spotify_resume_song()
    pass
