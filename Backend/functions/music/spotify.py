import os
import time
from base64 import b64encode
from dotenv import load_dotenv
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()


def exchange_spotify_auth_for_access():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    # Put https://doamin/KEY in .env file
    redirect_uri = 'http://localhost:8080/callback'
    scopes = "user-read-private playlist-read-private user-modify-playback-state"

    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri=http://localhost:8888/callback&scope=user-read-playback-state"
    print("Go to this URl")
    print(auth_url)
    print("Autherize and grab the string after code in URL. Past bellow:")

    authorization_code = input("Enter the authorization code(In URL): ")

    # Your registered redirect URI
    redirect_uri = "http://localhost:8888/callback"

    # Encode the client ID and client secret in base64
    auth_header = f"{client_id}:{client_secret}"
    encoded_auth_header = b64encode(auth_header.encode()).decode()

    # Construct the URL to exchange the authorization code for an access token
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri
    }

    headers = {
        "Authorization": f"Basic {encoded_auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Make the POST request to get the access token
    response = requests.post(token_url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        token_data = response.json()

        # Extract the access token and refresh token
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")

        os.environ["exchange_access_token"] = access_token
        os.environ["exchange_refresh_token"] = refresh_token

        print(f"Access Token: {access_token}")
        print(f"Refresh Token: {refresh_token}")
        return access_token
    else:
        print(f"Failed to get access token. Status code: {response.status_code}")
        print(response.text)


def get_spotify_access_token():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(url, headers=headers, data=data)

    return response.json()['access_token']


def control_spotify_api():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    # Spotify Authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri="http://localhost:8080",
                                                   scope="user-read-playback-state,user-modify-playback-state"))

    return sp


def get_spotify_player_id():
    api_session = exchange_spotify_auth_for_access()

    url = "https://api.spotify.com/v1/me/player/devices"
    headers = {"Authorization": "Bearer " + api_session}

    result = requests.get(url, headers=headers)

    list_of_devices = result.json()['devices']

    # Needs rewriting to enable device selection. Ex play in kitchen instead of the office.
    for device in list_of_devices:
        print(device)
        if "raspotify" in device["name"]:
            device_id = device['id']
            print(device_id)
            return device_id



def get_spotify_song(song_name):
    api_session = get_spotify_access_token()

    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + api_session}

    params = {
        "q": song_name,
        "type": "track",
        "limit": 1  # Number of results to return currently most played in spotify
    }

    result = requests.get(url, headers=headers, params=params)
    print(result.json())

    if result.status_code == 200:
        json_result = result.json()
        tracks = json_result['tracks']['items']

        track = tracks[0]  # Get the first track in the list
        song_info = {
            "track_id": track['id'],
            "track_name": track['name'],
            "artist_name": track['artists'][0]['name'],
            "album_name": track['album']['name'],
            "spotify_url": track['external_urls']['spotify'],

        }

        # os.system(f'start {spotify_url}')

        return song_info

    else:
        print(f"Failed to search for the song: {result.status_code}")


def play_spotify_song(song_name):
    song_details = get_spotify_song(song_name)
    spotify_track_id = song_details['track_id']
    song = song_details['track_name']
    artist = song_details['artist_name']

    if os.getenv('SPOTIFY_DEVICE_ID'):
        device_id = os.getenv('SPOTIFY_DEVICE_ID')
    else:
        device_id = get_spotify_player_id()

    cursor = control_spotify_api()
    cursor.start_playback(device_id=device_id, uris=[f'spotify:track:{spotify_track_id}'])

    return f"Playing {song} by {artist}"


if __name__ == '__main__':
    play_spotify_song("Clear My Head")
    # get_spotify_player_id()
    # exchange_spotify_auth_for_access()
    # pass
