import config
from scripts.database import DatabaseManager
import _csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
import csv
from datetime import datetime
import os

class SpotifyManager:
    def __init__(self):
        self.database_manager = DatabaseManager()
        self.database_manager.check_and_backup()

        self.sp = None
        self.current_scope = None  # Track the current scope
        self.current_playlist = None
        self.playlists = self.fetch_user_playlists()

    def authenticate_spotify(self, scope=None):
        """Authenticate with Spotify and return a Spotipy client."""
        if scope != self.current_scope:
            cache_handler = CacheFileHandler(cache_path="../.cache")
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=config.client_id,
                client_secret=config.client_secret,
                redirect_uri=config.redirect_uri,
                scope=scope,
                cache_handler=cache_handler,
            ))
            self.current_scope = scope  # Update the current scope

        return self.sp

    def fetch_user_playlists(self):
        self.authenticate_spotify("user-library-read playlist-read-private")
        user_id = self.sp.current_user()['id']

        limit = 50
        offset = 0

        playlists = self.sp.user_playlists(user=user_id, limit=limit, offset=offset)
        playlist_items = playlists['items']
        user_playlists = []

        for playlist in playlist_items:
            owner = playlist['owner']
            if owner['id'] == user_id:
                user_playlists.append(playlist)

        return user_playlists

    def select_playlist(self, playlist):
        self.current_playlist = playlist

    def save_playlist_to_file(self, playlist):
        """Download songs from a playlist and save them to a text file."""
        self.authenticate_spotify("playlist-read-private")
        playlist_id = playlist['id']

        offset = 0
        limit = 100
        all_tracks = []

        while True:
            results = self.sp.playlist_items(playlist_id, offset=offset, limit=limit, additional_types='track')
            tracks = results['items']

            if not tracks:
                break
            all_tracks.extend(tracks)
            offset += limit

        track_data = [
            ["track_id","track_name","artist","album","year",
                      "duration_ms","explicit","popularity"]
            ]

        for item in all_tracks:
            track = item['track']
            line = [
                track['id'],
                track['name'],
                track['artists'][0]['name'],
                track['album']['name'],
                track['album']['release_date'][:4],
                track['duration_ms'],
                track['explicit'],
                track['popularity']
            ]
            track_data.append(line)

        file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = f"{playlist['name']}.csv"
        full_path = os.path.join(file_path, filename)

        with open(full_path, 'w', encoding='utf-8', errors='ignore', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(track_data)

        return len(all_tracks)

    def import_playlist_from_file(self, input_file, separator, playlist_name,
                                  playlist_description):
        """Create a Spotify playlist from a file containing song names and artists."""
        try:
            self.authenticate_spotify("playlist-modify-public")
            user_id = self.sp.current_user()['id']

            def get_track_uri(song, artist):
                query = f"track:{song} artist:{artist}"
                print(f"Searching for: {query}")
                result = self.sp.search(q=query, type='track', limit=1,
                                        offset=0)

                if result['tracks']['items']:
                    print(
                        f"Found track: {result['tracks']['items'][0]['name']}")
                    return result['tracks']['items'][0]['uri']

                else:
                    print(f"No match found for {song} by {artist}")

                return None

            song_uris = []
            with open(input_file, 'r', encoding='utf-8') as file:
                if separator == "Auto":
                    try:
                        sample = file.read(1024)
                        sniffer = csv.Sniffer()
                        separator = sniffer.sniff(sample).delimiter
                        file.seek(0)

                    except _csv.Error:
                        return False, "Error detecting the separator. Enter separator manually."

                reader = csv.reader(file, delimiter=separator)
                for row in reader:
                    if len(row) == 2:
                        song_name = row[0].strip()
                        artist_name = row[1].strip()
                        track_uri = get_track_uri(song_name, artist_name)
                        if track_uri:
                            song_uris.append(track_uri)

            if song_uris:
                new_playlist = self.sp.user_playlist_create(user=user_id,
                                                            name=playlist_name,
                                                            public=True,
                                                            description=playlist_description)
                self.sp.playlist_add_items(new_playlist['id'], song_uris)
                return True, f"Playlist '{playlist_name}' created successfully with {len(song_uris)} songs."

            else:
                return False, "No songs found in the file."

        except Exception as e:
            return False, f"An error occurred: {e}"

    def make_playlist_private(self, playlist):
        self.authenticate_spotify("playlist-modify-public playlist-modify-private")

        try:
            self.sp.playlist_change_details(playlist['id'], public=False)
            return True, f"Playlist {playlist['name']} has been made private."

        except spotipy.exceptions.SpotifyException as e:
            return False, f"Error making playlist private: {e}"

    def remove_playlist(self, playlist):
        self.authenticate_spotify("playlist-modify-public playlist-modify-private")
        success = self.make_playlist_private(playlist)

        try:
            self.sp.current_user_unfollow_playlist(playlist['id'])
            return success[0], True, f"{success[1]}\nPlaylist {playlist['name']} removed from your library."

        except spotipy.exceptions.SpotifyException as e:
            return success[0], False, f"{success[1]}\nError removing playlist: {e}"

    def save_top_items_to_csv(self, item_type='tracks', limit=20,
                              time_range='medium_term',
                              file_name="top_items.csv"):
        """
        Save the user's top items (tracks or artists) to a CSV file.

        :param item_type: 'tracks' or 'artists' (default is 'tracks')
        :param limit: Number of top items to retrieve (default is 20)
        :param time_range: Over what time frame ('short_term', 'medium_term', 'long_term')
        :param file_name: The name of the CSV file to save data to (default is 'top_items.csv')
        """
        self.authenticate_spotify("user-top-read")

        # Fetch top items
        if item_type == 'tracks':
            top_items = self.sp.current_user_top_tracks(limit=limit,
                                                        time_range=time_range)[
                'items']
            headers = ['Track Name', 'Artist', 'Album', 'Popularity']
            rows = [[track['name'], track['artists'][0]['name'],
                     track['album']['name'], track['popularity']]
                    for track in top_items]

        elif item_type == 'artists':
            top_items = self.sp.current_user_top_artists(limit=limit,
                                                         time_range=time_range)[
                'items']
            headers = ['Artist Name', 'Genres', 'Popularity']
            rows = [[artist['name'], ", ".join(artist['genres']),
                     artist['popularity']]
                    for artist in top_items]

        else:
            raise ValueError("item_type must be 'tracks' or 'artists'.")

        # Save to CSV
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

    def fetch_last_played_tracks(self, limit=50):
        """
        Retrieve the user's recently played tracks, filtering out consecutive duplicate plays.

        :param limit: Number of recent tracks to retrieve (default is 50)
        :return: List of dictionaries containing track name, artist, and played time, without consecutive duplicates
        """
        self.authenticate_spotify("user-read-recently-played")

        try:
            recent_tracks = \
            self.sp.current_user_recently_played(limit)['items']
            filtered_tracks = []
            last_track_id = None

            for track_info in recent_tracks:
                track = track_info['track']
                played_at = track_info.get('played_at')
                if not played_at:
                    continue  # Skip tracks without 'played_at'

                played_at = datetime.strptime(played_at,"%Y-%m-%dT%H:%M:%S.%fZ")

                # Check for consecutive duplicates
                if track['id'] != last_track_id:
                    filtered_tracks.append({
                        'track_id': track['id'],
                        'track_name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'album': track['album']['name'],
                        'year': track['album']['release_date'][:4],
                        'duration_ms': track['duration_ms'],
                        'explicit': track['explicit'],
                        'popularity': track['popularity'],
                        'played_at': played_at,
                    })
                    last_track_id = track['id']

                if len(filtered_tracks) >= limit:  # Stop once we have enough tracks after filtering
                    break

            return filtered_tracks

        except spotipy.exceptions.SpotifyException as e:
            print(f"Error fetching recent tracks: {e}")
            return []

    def save_recent_play_to_database(self, track_info):
        # Assume track_info is a dictionary with details about the track
        self.database_manager.insert_play(
            track_id=track_info['track_id'],
            track_name=track_info['track_name'],
            artist=track_info['artist'],
            album=track_info['album'],
            year=track_info['year'],
            duration_ms=track_info['duration_ms'],
            explicit=track_info['explicit'],
            popularity=track_info['popularity'],
            played_at=track_info['played_at'],
            session_id=track_info.get('session_id')  # Optional session_id
        )

    def update_play_history(self, file=None):
        # Get the latest `played_at` timestamp from the database
        latest_played_at = self.database_manager.get_most_recent_play_timestamp() or datetime.min

        if file is None:
            # Fetch recent plays from Spotify
            recent_tracks = self.fetch_last_played_tracks()

        else:
            recent_tracks = []
            try:
                with open(file, mode='r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f, delimiter=';')
                    for row in reader:
                        # Confirm `row` is a dictionary and `played_at` key exists
                        if isinstance(row, dict) and 'played_at' in row:
                            row['played_at'] = datetime.strptime(row['played_at'], "%Y-%m-%d %H:%M:%S.%f")
                        recent_tracks.append(row)

            except FileNotFoundError:
                print(f"Error: The file '{file}' was not found.")

            except csv.Error as e:
                print(f"Error reading CSV file at line {reader.line_num}: {e}")

            except Exception as e:
                print(f"An unexpected error occurred: {e}")


        # Filter out tracks that have already been stored
        new_tracks = [
            track for track in recent_tracks
            if track['played_at'] > latest_played_at
        ]

        # Sort new_tracks by played_at to ensure chronological order
        new_tracks.sort(key=lambda track: track['played_at'])

        for track_info in new_tracks:
            self.save_recent_play_to_database(track_info)

        print(
            f"Stored {len(new_tracks)} new tracks.")

    def show_recent_plays(self):
        recent_plays = self.database_manager.get_recent_plays(limit=20)
        for play in recent_plays:
            print(f"{play[1]} by {play[2]}, played at {play[3]}")
