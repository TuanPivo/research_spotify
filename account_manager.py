import json
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from cryptography.fernet import Fernet
import config

class AccountManager:
    def __init__(self):
        self.accounts = {}
        self.tokens = {}
        self.proxies = []
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.load_accounts()
        self.load_proxies()

    def load_accounts(self):
        try:
            with open(config.ACCOUNTS_FILE, 'r') as f:
                encrypted_data = json.load(f)
                self.accounts = {k: self.cipher_suite.decrypt(v.encode()).decode() 
                               for k, v in encrypted_data.items()}
        except FileNotFoundError:
            self.accounts = {}

    def save_accounts(self):
        encrypted_data = {k: self.cipher_suite.encrypt(v.encode()).decode() 
                         for k, v in self.accounts.items()}
        with open(config.ACCOUNTS_FILE, 'w') as f:
            json.dump(encrypted_data, f)

    def load_proxies(self):
        try:
            with open('proxy.txt', 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.proxies = []

    def add_account(self, username, password):
        self.accounts[username] = password
        self.save_accounts()

    def get_random_proxy(self):
        if not self.proxies:
            return None
        proxy = random.choice(self.proxies)
        if config.PROXY_USERNAME and config.PROXY_PASSWORD:
            return f"http://{config.PROXY_USERNAME}:{config.PROXY_PASSWORD}@{proxy}"
        return f"http://{proxy}"

    def get_spotify_client(self, username):
        if username not in self.accounts:
            raise ValueError(f"Account {username} not found")

        proxy = self.get_random_proxy()
        proxies = {'http': proxy, 'https': proxy} if proxy else None

        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=config.SPOTIFY_CLIENT_ID,
                client_secret=config.SPOTIFY_CLIENT_SECRET,
                redirect_uri=config.SPOTIFY_REDIRECT_URI,
                username=username,
                scope='playlist-modify-public user-modify-playback-state',
                cache_handler=spotipy.CacheFileHandler(f"cache_{username}")
            ),
            requests_session=True,
            proxies=proxies
        )

    def create_playlist(self, username, name=None, description=None):
        sp = self.get_spotify_client(username)
        user_id = sp.current_user()['id']
        
        playlist = sp.user_playlist_create(
            user=user_id,
            name=name or config.DEFAULT_PLAYLIST_NAME,
            description=description or config.DEFAULT_PLAYLIST_DESCRIPTION
        )
        return playlist['id']

    def add_song_to_playlist(self, username, playlist_id, track_uri):
        sp = self.get_spotify_client(username)
        sp.playlist_add_items(playlist_id, [track_uri])

    def play_song(self, username, track_uri):
        sp = self.get_spotify_client(username)
        sp.start_playback(uris=[track_uri]) 