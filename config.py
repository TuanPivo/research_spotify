import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')

# Proxy settings
PROXY_LIST = []  # Will be populated from proxy.txt
PROXY_USERNAME = os.getenv('PROXY_USERNAME')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')

# Account settings
ACCOUNTS_FILE = 'accounts.json'
TOKENS_FILE = 'tokens.json'

# Playlist settings
DEFAULT_PLAYLIST_NAME = "Auto Generated Playlist"
DEFAULT_PLAYLIST_DESCRIPTION = "Automatically generated playlist"

# Application settings
MAX_CONCURRENT_ACCOUNTS = 1000
REQUEST_TIMEOUT = 30  # seconds 