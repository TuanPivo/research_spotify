# Spotify Playlist Manager

A Python application for managing multiple Spotify accounts, creating playlists, and managing songs across accounts using proxies.

## Prerequisites

1. **Python Environment**
   - Python 3.7 or higher
   - pip (Python package manager)

2. **Spotify Developer Account**
   - Create an account at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new application
   - Get Client ID and Client Secret
   - Add `http://localhost:8888/callback` to Redirect URIs

3. **Proxy Requirements**
   - List of working proxies (residential proxies recommended)
   - Proxy authentication credentials (if required)

4. **Docker (Optional)**
   - Docker Engine
   - Docker Compose

## Installation

### Option 1: Direct Installation

1. **Clone the repository and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup:**
   Create a `.env` file with the following content:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
   PROXY_USERNAME=your_proxy_username
   PROXY_PASSWORD=your_proxy_password
   ```

3. **Proxy Configuration:**
   Update `proxy.txt` with your proxy list in the format:
   ```
   ip1:port1
   ip2:port2
   ip3:port3
   ```

### Option 2: Docker Installation

1. **Create necessary directories and files:**
   ```bash
   mkdir -p data
   touch data/accounts.json data/tokens.json
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

   To run in detached mode:
   ```bash
   docker-compose up -d
   ```

   To stop the application:
   ```bash
   docker-compose down
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

## Running the Application

### Direct Method
```bash
python main.py
```

### Docker Method
```bash
docker-compose up
```

2. **First-time Setup:**
   - The application will create necessary files:
     - `accounts.json` (encrypted account storage)
     - `tokens.json` (Spotify tokens)
     - Cache files for each account

## Using the Application

### Account Management Tab
1. Enter Spotify username and password
2. Click "Add Account" to store the account
3. Accounts are automatically encrypted before storage

### Playlist Management Tab
1. **Creating Playlists:**
   - Enter playlist name and description
   - Click "Create Playlist"
   - Note the playlist ID from the status display

2. **Adding Songs:**
   - Get Spotify Track URI:
     - Right-click song in Spotify
     - Select "Share"
     - Choose "Copy Spotify URI"
   - Enter the URI in the input field
   - Click "Add Song"

3. **Playing Songs:**
   - Enter the track URI
   - Click "Play Song"
   - Note: Requires Spotify Premium account

## Important Notes

### Security
- Never share your `.env` file
- Keep `accounts.json` secure (contains encrypted credentials)
- Regularly update proxy list
- Use strong passwords for accounts

### Proxy Management
- Each account uses a random proxy
- Recommended: Use residential proxies
- Monitor proxy performance
- Update proxy list regularly

### Rate Limits
- Spotify API has rate limits
- Using multiple accounts may trigger rate limits
- Use proxies to distribute requests
- Monitor status display for errors

### Troubleshooting

1. **Authentication Errors:**
   - Check Spotify API credentials
   - Verify redirect URI matches
   - Ensure account credentials are correct

2. **Proxy Errors:**
   - Verify proxy list format
   - Check proxy authentication
   - Test proxy connectivity

3. **Playback Issues:**
   - Ensure Premium account
   - Check active device
   - Verify track URI format

4. **Common Error Messages:**
   - "Invalid client": Check API credentials
   - "Invalid redirect URI": Update in Spotify Dashboard
   - "Proxy error": Check proxy configuration
   - "Rate limit exceeded": Wait or use different proxy

## File Structure
```
├── main.py              # Main application
├── account_manager.py   # Account management logic
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── proxy.txt          # Proxy list
├── data/              # Data directory
│   ├── accounts.json  # Encrypted account storage
│   └── tokens.json    # Spotify tokens
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
└── .dockerignore     # Docker ignore file
```

## Best Practices

1. **Account Management:**
   - Use unique passwords
   - Regular password updates
   - Monitor account activity

2. **Proxy Usage:**
   - Rotate proxies regularly
   - Monitor proxy performance
   - Use reliable proxy providers

3. **Application Maintenance:**
   - Regular dependency updates
   - Monitor error logs
   - Backup account data

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all configurations
3. Review error messages in status display

## Updates and Maintenance

Regular maintenance tasks:
1. Update Python dependencies
2. Refresh proxy list
3. Monitor Spotify API changes
4. Backup account data
5. Check for security updates 