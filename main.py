import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLineEdit, QLabel,
                            QTextEdit, QMessageBox, QTabWidget)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from account_manager import AccountManager

class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(str(result))
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.account_manager = AccountManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Spotify Playlist Manager')
        self.setGeometry(100, 100, 800, 600)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Account Management Tab
        account_tab = QWidget()
        account_layout = QVBoxLayout(account_tab)
        
        # Add Account Section
        add_account_group = QWidget()
        add_account_layout = QHBoxLayout(add_account_group)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Spotify Username')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Spotify Password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        add_account_btn = QPushButton('Add Account')
        add_account_btn.clicked.connect(self.add_account)
        
        add_account_layout.addWidget(self.username_input)
        add_account_layout.addWidget(self.password_input)
        add_account_layout.addWidget(add_account_btn)
        
        account_layout.addWidget(add_account_group)
        
        # Playlist Management Tab
        playlist_tab = QWidget()
        playlist_layout = QVBoxLayout(playlist_tab)
        
        # Create Playlist Section
        create_playlist_group = QWidget()
        create_playlist_layout = QHBoxLayout(create_playlist_group)
        
        self.playlist_name_input = QLineEdit()
        self.playlist_name_input.setPlaceholderText('Playlist Name')
        self.playlist_desc_input = QLineEdit()
        self.playlist_desc_input.setPlaceholderText('Playlist Description')
        
        create_playlist_btn = QPushButton('Create Playlist')
        create_playlist_btn.clicked.connect(self.create_playlist)
        
        create_playlist_layout.addWidget(self.playlist_name_input)
        create_playlist_layout.addWidget(self.playlist_desc_input)
        create_playlist_layout.addWidget(create_playlist_btn)
        
        playlist_layout.addWidget(create_playlist_group)
        
        # Add Song Section
        add_song_group = QWidget()
        add_song_layout = QHBoxLayout(add_song_group)
        
        self.song_uri_input = QLineEdit()
        self.song_uri_input.setPlaceholderText('Spotify Track URI')
        
        add_song_btn = QPushButton('Add Song')
        add_song_btn.clicked.connect(self.add_song)
        
        play_song_btn = QPushButton('Play Song')
        play_song_btn.clicked.connect(self.play_song)
        
        add_song_layout.addWidget(self.song_uri_input)
        add_song_layout.addWidget(add_song_btn)
        add_song_layout.addWidget(play_song_btn)
        
        playlist_layout.addWidget(add_song_group)
        
        # Status Display
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        playlist_layout.addWidget(self.status_display)
        
        # Add tabs
        tabs.addTab(account_tab, "Account Management")
        tabs.addTab(playlist_tab, "Playlist Management")

    def add_account(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')
            return
        
        try:
            self.account_manager.add_account(username, password)
            self.status_display.append(f"Account {username} added successfully")
            self.username_input.clear()
            self.password_input.clear()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add account: {str(e)}')

    def create_playlist(self):
        name = self.playlist_name_input.text()
        description = self.playlist_desc_input.text()
        
        if not name:
            QMessageBox.warning(self, 'Error', 'Please enter a playlist name')
            return
        
        worker = WorkerThread(self.account_manager.create_playlist, 
                            self.username_input.text(), name, description)
        worker.finished.connect(lambda result: self.status_display.append(f"Playlist created: {result}"))
        worker.error.connect(lambda error: QMessageBox.critical(self, 'Error', f'Failed to create playlist: {error}'))
        worker.start()

    def add_song(self):
        track_uri = self.song_uri_input.text()
        
        if not track_uri:
            QMessageBox.warning(self, 'Error', 'Please enter a track URI')
            return
        
        worker = WorkerThread(self.account_manager.add_song_to_playlist,
                            self.username_input.text(), track_uri)
        worker.finished.connect(lambda result: self.status_display.append(f"Song added successfully"))
        worker.error.connect(lambda error: QMessageBox.critical(self, 'Error', f'Failed to add song: {error}'))
        worker.start()

    def play_song(self):
        track_uri = self.song_uri_input.text()
        
        if not track_uri:
            QMessageBox.warning(self, 'Error', 'Please enter a track URI')
            return
        
        worker = WorkerThread(self.account_manager.play_song,
                            self.username_input.text(), track_uri)
        worker.finished.connect(lambda result: self.status_display.append(f"Song started playing"))
        worker.error.connect(lambda error: QMessageBox.critical(self, 'Error', f'Failed to play song: {error}'))
        worker.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 