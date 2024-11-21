from scripts.backend import SpotifyManager
import os


class SpotifyCLI:
    def __init__(self):
        """Initialize the Spotify CLI with SpotifyManager."""
        self.spotify_manager = SpotifyManager()

    def show_main_menu(self):
        """Show the main menu and handle user choice."""
        while True:

            if self.spotify_manager.current_playlist:
                print("\nSelected playlist: ",
                      self.spotify_manager.current_playlist['name'])
                print()

            print("\nSpotify Manager CLI")
            print("1. View Playlists")
            print("2. Create New Playlist")
            print("3. Download Playlist")
            print("4. Delete Playlist")
            print("5. Save Top Items to CSV")
            print("6. View Last Played Tracks")
            print("7. Fetch and Store Recent Tracks")
            print("8. Exit")

            choice = input("Enter your choice: ")
            if choice == '1':
                self.list_playlists()
            elif choice == '2':
                self.create_playlist()
            elif choice == '3':
                self.download_playlist()
            elif choice == '4':
                self.delete_playlist()
            elif choice == '5':
                self.save_top_items_to_csv()
            elif choice == '6':
                self.view_recent_tracks()
            elif choice.startswith('7'):
                file = choice.split(' ')[1] if ' ' in choice else None
                self.fetch_and_store_recent_tracks(file)
            elif choice == '8':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice, please try again.")

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def list_playlists(self):
        """List all playlists and select one to view."""
        self.clear_console()

        playlists = self.spotify_manager.fetch_user_playlists()
        if not playlists:
            print("No playlists found.")
            return

        print("\nPlaylists:")
        for i, playlist in enumerate(playlists, 1):
            print(f"{i}. {playlist['name']}")

        try:
            choice = int(
                input("Select a playlist number to view (or 0 to go back): "))
            if choice == 0:
                self.clear_console()
                return
            self.clear_console()
            self.spotify_manager.select_playlist(playlists[choice - 1])
            print(f"\nPlaylist {self.spotify_manager.current_playlist['name']} selected successfully.")

        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")

    def create_playlist(self):
        """Prompt user to create a new playlist."""
        self.clear_console()

        file_path = input("Enter the path to the text file with song names: ")
        playlist_name = input("Enter the playlist name: ") or "New Playlist"
        playlist_desc = input(
            "Enter the playlist description: ") or "No description"
        separator = input(
            "Enter separator used in the file (leave empty for default): ") or "Auto"

        success = self.spotify_manager.import_playlist_from_file(file_path,
                                                                 separator,
                                                                 playlist_name,
                                                                 playlist_desc)

        self.clear_console()

        if success[0]:
            print("Playlist created successfully!")
        else:
            print("Error:", success[1])

    def download_playlist(self):
        """Download the selected playlist's songs to a file."""
        self.clear_console()

        if not self.spotify_manager.current_playlist:
            print("No playlist selected. Please select a playlist first.")
            return

        try:
            num_songs = self.spotify_manager.save_playlist_to_file(
                self.spotify_manager.current_playlist)
            print(
                f"{num_songs} songs downloaded to {self.spotify_manager.current_playlist['name']}.txt")

        except ValueError as e:
            print("Error:", str(e))

    def delete_playlist(self):
        """Delete the selected playlist."""
        self.clear_console()

        if not self.spotify_manager.current_playlist:
            print("No playlist selected. Please select a playlist first.")
            return

        try:
            success = self.spotify_manager.remove_playlist(
                self.spotify_manager.current_playlist)
            print(success[2])  # Assuming success[2] contains success message
            self.spotify_manager.current_playlist = None

        except ValueError as e:
            print("Error:", str(e))

    def save_top_items_to_csv(self):
        """Prompt user to save their top items to a CSV file."""
        self.clear_console()

        print("\nSave Top Items to CSV")

        item_type = input(
            "Enter item type ('tracks' or 'artists'): ").strip().lower()

        if item_type not in ['tracks', 'artists']:
            print("Invalid item type. Please choose 'tracks' or 'artists'.")
            return

        try:
            limit = int(input(
                "Enter the number of top items to retrieve (e.g., 10, 20): "))
            if limit <= 0:
                raise ValueError

        except ValueError:
            print("Invalid number. Please enter a positive integer.")
            return

        time_range = input(
            "Enter time range ('short_term', 'medium_term', 'long_term'): ").strip().lower()

        if time_range not in ['short_term', 'medium_term', 'long_term']:
            print("Invalid time range. Choose 'short_term', 'medium_term', or 'long_term'.")
            return

        file_name = input(
            "Enter the filename to save the CSV (default is 'top_items.csv'): ") or "top_items.csv"

        self.clear_console()

        try:
            self.spotify_manager.save_top_items_to_csv(item_type=item_type,
                                                       limit=limit,
                                                       time_range=time_range,
                                                       file_name=file_name)
            print(f"Top {item_type} saved to {file_name}")

        except Exception as e:
            print(f"An error occurred while saving top items: {e}")

    def view_recent_tracks(self):
        """Fetch and display the user's recently played tracks."""
        self.clear_console()

        print("\nLast Played Tracks")
        try:
            limit = int(input(
                "Enter the number of recent tracks to display (default is 10): ") or 10)
            if limit <= 0:
                raise ValueError("Limit must be a positive integer.")

        except ValueError:
            print("Invalid input. Please enter a positive integer.")
            return

        recent_tracks = self.spotify_manager.fetch_last_played_tracks(
            limit=limit)

        self.clear_console()

        if recent_tracks:
            print("\nRecently Played Tracks:")
            for track in recent_tracks:
                print(
                    f"{track['track_name']} by {track['artist']} (Played At: {track['played_at']})")

        else:
            print("No recently played tracks found.")

    def fetch_and_store_recent_tracks(self, file=None):
        self.clear_console()
        self.spotify_manager.update_play_history(file)


if __name__ == "__main__":
    app = SpotifyCLI()
    app.show_main_menu()
