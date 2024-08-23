import configparser
import datetime
import os
import sys
import spotipy

from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth
import time


def create_config():
    # Create a new configuration file
    config = configparser.ConfigParser()

    client_id = input("Enter your Spotify client ID: ")
    client_secret = input("Enter your Spotify client secret: ")
    playlist_url = input("Enter your Release Radar playlist URL: ")

    # Set the default configuration values
    config["Spotify"] = {
        "client_id": client_id,
        "client_secret": client_secret,
        "release_radar_url": playlist_url,
        "redirect_uri": "http://localhost:8080"
    }

    # Write the configuration to a file
    with open("config.ini", "w") as file:
        config.optionxform = str  # Preserve case sensitivity
        config.write(file)


def read_config():
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read("config.ini")

    if not config.has_section("Spotify"):
        print("Error: The configuration file is missing the [Spotify] section.")
        sys.exit(1)

    # Get the Spotify API credentials from the configuration file
    client_id = config.get("Spotify", "client_id")
    client_secret = config.get("Spotify", "client_secret")
    redirect_uri = config.get("Spotify", "redirect_uri")

    # Validate the Spotify API credentials
    if not client_id or not client_secret or not redirect_uri:
        print("Error: Invalid Spotify API credentials.")
        sys.exit(1)

    if config.has_option("Spotify", "release_radar_url"):
        playlistID = config.get("Spotify", "release_radar_url")

    return client_id, client_secret, redirect_uri, playlistID


def get_playlist_name(playlist_url, sp):
    # Get the playlist metadata
    try:
        playlist = sp.playlist(playlist_url)
    except SpotifyException:
        print("Error: The playlist does not exist or could not be accessed.")
        sys.exit(1)
    except Exception as e:
        print(f"Spotify client {str(e)}")
        sys.exit(1)

    return playlist["name"]


def get_playlist_tracks(playlist_url, playlist_name, sp):
    limit = 100  # Maximum number of tracks per API request
    offset = 0
    list_tracks = []

    while True:
        # Get the playlist tracks
        try:
            dirty_list = sp.playlist_tracks(playlist_url, offset=offset, limit=limit)
        except SpotifyException:
            print(
                f"Error: The playlist with ID {playlist_url} does not exist or could not be accessed."
            )

            sys.exit(1)

        if dirty_list["total"] == 0:
            print(f"Playlist '{playlist_name}' does not contain any tracks.")
            sys.exit(1)

        for item in dirty_list["items"]:
            track_id = item["track"]["id"]
            list_tracks.append(track_id)

        # Check if we need to fetch more tracks
        if len(dirty_list["items"]) < limit:
            break

        # Update the offset for the next request
        offset += limit

    return list_tracks


def createNewPlaylist(sp, playlist_name, playlist_tracks):
    # Get the current user's ID
    user_id = sp.current_user()["id"]

    # Create a new playlist
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    playlist_url = playlist["id"]

    # Add tracks to the playlist
    total_tracks = len(playlist_tracks)
    added_tracks = 0
    for track in playlist_tracks:
        sp.playlist_add_items(playlist_url, [track])
        added_tracks += 1
        progress = (added_tracks / total_tracks) * 100
        print(f"Adding tracks to playlist: {progress:.2f}% complete", end="\r")
        time.sleep(0.1)

    print(f"\nPlaylist '{playlist_name}' created successfully with {total_tracks} tracks.")


def main():
    # Ensure config.ini exists
    if not os.path.isfile("config.ini"):
        create_config()

    client_id, client_secret, redirect_uri, playlistID = read_config()

    # Create a Spotify client
    try:
        # Create a Spotify client with OAuth
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-modify-private"
        ))
    except SpotifyException:
        print("Error: Invalid Spotify API credentials.")
        sys.exit(1)

    # Get the playlist name and tracks
    playlist_name = get_playlist_name(playlistID, sp)

    # Append date to playlist name
    playlist_name = f"{playlist_name} - {datetime.datetime.now().strftime('%Y-%m-%d')}"

    print(f"Analyzing playlist '{playlist_name}'.")

    # Get the playlist tracks
    playlistTracks = get_playlist_tracks(playlistID, playlist_name, sp)

    # Create a new playlist with the same tracks
    createNewPlaylist(sp, playlist_name, playlistTracks)


if __name__ == "__main__":
    main()
