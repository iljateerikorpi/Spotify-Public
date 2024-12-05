# Spotify Manager
[![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-blue)](https://creativecommons.org/licenses/by-nc/4.0/)


This project uses Spotify's API to track recently played songs and manage playlists by downloading songs or creating new playlists from a text file. To use the Spotify API, you need to set up a configuration file with your Spotify credentials.

## Requirements

- Python 3.x
- `spotipy` library

You can install the required packages by running:

```bash
pip install -r requirements.txt
```

## File Structure
```bash
project_root/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── config.py
├── database/                      # Automatically created during program
│   ├── spotify_plays.db           # Database file(s)
│   └── csv_backups/               # Directory for CSV backups
└── scripts/
    ├── automation_scripts/        # Only for reference (not included in requirements)
    ├── backend.py                 # Main logic for interacting with Spotify API
    ├── database.py                # DatabaseManager class
    └── cli.py                     # Command-line interface script

```

## Configuration
To configure your Spotify credentials the config.py file should contain the following variables:
```python
# Spotify credentials
client_id = 'your_client_id'
client_secret = 'your_client_secret'
redirect_uri = 'http://localhost:8080/callback/'  # Or another redirect URI as per your Spotify app settings
```

## How to get your Spotify credentials
1. Visit https://developer.spotify.com/dashboard/applications and create an application.
2. Use the Client ID and Client secret provided in the dashboard.
3. Set the redirect_uri to match the one configured in your Spotify app.

## How to Run
Once the configuration file is set up, you can run the program using:
```bash
python -m scripts.cli
```

## Input File Format

When creating a new playlist from a file, the input file must be in a specific format. Each line of the file should contain a **song name** and an **artist name**, separated by a character such as a comma or a semicolon.

### Example:
```markdown
Song Name 1, Artist Name 1
Song Name 2, Artist Name 2
```


### Important Notes:
- The file must not contain additional information such as featured artists, release years, or album names.
- Only the main artist should be listed for each song.
- The separator (e.g., comma, semicolon) must be consistent throughout the file.
- Any unnecessary spaces before or after the song or artist names will be automatically stripped, so don’t worry about extra spaces.
- You will be prompted to specify the separator when running the program.

### Invalid Example:
```markdown
Song Name (feat. Featured Artist), Artist Name
Song Name (Live), Artist Name
```
In the above example, "feat. Featured Artist" and "(Live)" should be removed, as only the main artist and the song name should be provided.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.  
You can view the full license [here](https://creativecommons.org/licenses/by-nc/4.0/).

## Author

Created and maintained by [Ilja Teerikorpi](https://github.com/iljateerikorpi).  
