# ReleaseRadar

Fix for Spotify's broken Release Radar playlist. Will copy the complete playlist to a new playlist called "Release Radar - &lt;DATE>".

## Required Package

- [spotipy](https://pypi.org/project/spotipy/)

## Installation

1. Clone this repository:

    `git clone <https://github.com/mpusch88/ReleaseRadar>`

2. Install the required Python package:

    `pip install spotipy`

3. Create a Spotify application and get your client ID and client secret. You can do this by logging in to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and creating a new application. Note that the name and description of the application do not matter.

4. (Optional) Create an alias to launch the script:

PowerShell - Add the following line to your profile file (e.g. `Microsoft.PowerShell_profile.ps1`):

```powershell
function rr {
  cd "<path_to_releaseRadar>"; & python ReleaseRadar.py
}
```

ZSH - Add the following line to your `.zshrc` file:

```zsh
alias rr="python <path_to_releaseRadar>/ReleaseRadar.py"
```

Bash - Add the following line to your `.bashrc` file:

```bash
alias rr="python <path_to_releaseRadar>/ReleaseRadar.py"
```

## Configuration

The program can be configured via the generated `config.ini` file.

The `config.ini` file should be located in the same directory as `ReleaseRadar.py` and should have the following format:

```ini
client_id = your_spotify_client_id
client_secret = your_spotify_client_secret
playlist = your_spotify_playlist_id
```

Where:

- `client_id` is your Spotify application's client ID. (example: `client_id = 1234567890abcdef1234567890abcdef`)
- `client_secret` is your Spotify application's client secret. (example: `client_secret = 987654321`)
- `release_radar_id` (Optional) The Spotify playlist ID of your ReleaseRadar playlist. (example: `release_radar_id = https://open.spotify.com/playlist/37i9dQZEVXbcVlACDEuMlx?si=6ba5e8dfbd4442da`)

## Usage

The program can be run from the command line using the following command:

```bash
python ReleaseRadar.py
```

If an alias was created, the program can be run using the following command:

```bash
rr
```

Note that running this script will generate a cache file in the same directory as `ReleaseRadar.py` called `.cache`. This fle is used to store thei user's Spotify access token and should not be deleted.
