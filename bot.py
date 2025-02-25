import os
import dotenv

dotenv.load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from pprint import pprint


SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))


def get_playlist_tracks(username, playlist_id):
    i = 1
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        if i % 5 == 0: print(i*100, "tracks found...")
        i += 1
        results = sp.next(results)
        tracks.extend(results['items'])
    print(f"Playlist Length: {len(tracks)}\n")
    return tracks


def saveFailedArtist(artist):
    print(f"Failed to get artist info for {artist['name']}: {artist['id']}")
    print("Skipping...")
    
    with open("failed_artists.txt", "a") as f:
        f.write(f"{artist['name']}: {artist['id']}\n")

def main():
    playlist_id = "4pA4z4soUdFWWMnS5JzWXT"
    username = "orangeblackcow"
    
    tracks = get_playlist_tracks(username, playlist_id)
    artists = {}

    print("Finding the least popular artist in the playlist...")

    for i in range(0, len(tracks), 50):
        artists_ids = []
        artists_names = []
        for j in range(50):
            temp = tracks[i+j]["track"]["artists"]
            for artist in temp:
                if artist["id"] is None:
                    saveFailedArtist(artist)
                if artist["id"] not in artists_ids and artist["name"] not in artists:
                    artists_ids.append(artist["id"])
                    artists_names.append(artist["name"])
        
        try:
            found_artists = sp.artists(artists_ids)
            for artist_name, artist_info in zip(artists_names, found_artists["artists"]):
                artists[artist_name] = artist_info["followers"]["total"]
            
        except Exception as e:
            saveFailedArtist(artist)

        print(f"{(i+1) * 50} tracks processed...")

    least_popular = min(artists, key=artists.get)
    print(f"\nLeast popular artist: {least_popular} with {artists[least_popular]} followers")
    
    with open("artists.txt", "w") as f:
        for artist in artists:
            f.write(f"{artist}: {artists[artist]}\n")


def main():
    playlist_id = "4pA4z4soUdFWWMnS5JzWXT"
    username = "orangeblackcow"
    
    tracks = get_playlist_tracks(username, playlist_id)
    artists = {}

    print("Finding the least popular artist in the playlist...")

    i = 1
    for item in tracks:
        if i % 100 == 0: print(f"{i} tracks processed...")
        i += 1

        artist = item["track"]["artists"][0]
        artist_id = artist["id"]
        artist_name = artist["name"]

        try:
            if artist_name not in artists:
                if artist_id is None:
                    raise ValueError(f"Artist ID is None for {artist_name}")
                artist_info = sp.artist(artist_id)
                artists[artist_name] = artist_info["followers"]["total"]
            
        except Exception as e:
            saveFailedArtist(artist)   

    least_popular = min(artists, key=artists.get)
    print(f"\nLeast popular artist: {least_popular} with {artists[least_popular]} followers")
    
    with open("artists.txt", "w") as f:
        for artist in artists:
            f.write(f"{artist}: {artists[artist]}\n")


if __name__ == "__main__":
    main()