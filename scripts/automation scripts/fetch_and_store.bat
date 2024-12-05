@echo off
set PYTHONPATH=%PYTHONPATH%;your_path
python -c "from scripts.backend import SpotifyManager; SpotifyManager().update_play_history()"