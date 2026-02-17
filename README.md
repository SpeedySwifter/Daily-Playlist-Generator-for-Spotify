# 🎧 Daily Playlist Generator for Spotify

> Automatically create personalized Spotify playlists every day based on your listening history

Wake up to a fresh playlist of yesterday's favorite tracks – automatically generated and ready to play. No manual work, no configuration needed after initial setup.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Spotify API](https://img.shields.io/badge/Spotify-API-green.svg)](https://developer.spotify.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-orange.svg)](https://github.com/features/actions)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📸 Preview

```
🎵 Daily Mix - 2026-02-17
├── 🎵 Song you played yesterday at 23:45
├── 🎵 Another favorite from 18:30
├── 🎵 Your workout jam from 12:15
└── ... (all your yesterday's tracks)

✅ Created automatically at 8:00 AM (MEZ)
✅ Saved to your Spotify account
✅ Ready to play on any device
```

---

## ✨ Features

- 🤖 **Fully Automated** – Runs daily via GitHub Actions (free, forever)
- 🎵 **Personalized Playlists** – Based on your actual listening history
- 📅 **Daily Updates** – New playlist every morning at 8:00 AM (MEZ)
- 🔒 **Privacy First** – All data stays in your Spotify account
- ⚡ **Zero Maintenance** – Set it up once, enjoy forever
- 🎨 **Customizable** – Filter by mood, genre, time of day
- 📊 **Two Modes** – Daily playlists or 6-month retrospectives

---

## 🚀 Quick Start

### 1️⃣ Fork this Repository

Click the **Fork** button at the top right of this page.

### 2️⃣ Create Spotify Developer App

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click **"Create an App"**
3. Enter app details:
   - **App Name:** `Daily Playlist Generator`
   - **Redirect URI:** `http://localhost:8888/callback`
4. Save your **Client ID** and **Client Secret**

### 3️⃣ Generate Refresh Token

Run this script **once** on your local machine:

```python
# get_refresh_token.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp_oauth = SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8888/callback",
    scope="user-library-read user-read-recently-played playlist-modify-private playlist-modify-public"
)

token_info = sp_oauth.get_access_token(as_dict=True)
print("🎉 Your Refresh Token:", token_info['refresh_token'])
```

**Steps:**
```bash
# Install dependencies
pip install spotipy

# Run script
python get_refresh_token.py

# Follow browser authentication
# Copy the Refresh Token from output
```

### 4️⃣ Add GitHub Secrets

Go to your forked repository:

**Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these three secrets:

| Secret Name | Value |
|-------------|-------|
| `SPOTIFY_CLIENT_ID` | Your Spotify Client ID |
| `SPOTIFY_CLIENT_SECRET` | Your Spotify Client Secret |
| `SPOTIFY_REFRESH_TOKEN` | Your generated Refresh Token |

### 5️⃣ Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. That's it! ✅

---

## ⚙️ Configuration

### Schedule (when playlists are created)

Edit `.github/workflows/playlist.yml`:

```yaml
on:
  schedule:
    - cron: '0 6 * * *'  # 06:00 UTC = 08:00 MEZ
```

**Common schedules:**
- `0 6 * * *` – Daily at 8:00 AM (MEZ)
- `0 0 * * *` – Daily at midnight
- `0 12 * * 1` – Every Monday at noon

### Playlist Settings

Edit `generate_playlist.py`:

```python
# Playlist visibility
public_playlist = False  # True = public, False = private

# Playlist name format
playlist_name = f"Daily Mix - {yesterday}"

# Number of tracks (0 = all)
max_tracks = 50  # Limit to 50 songs, or 0 for unlimited
```

---

## 🎯 How It Works

```
┌─────────────┐
│   You listen│
│  to Spotify │
└──────┬──────┘
       │
       │ Spotify tracks your history
       │
       ▼
┌─────────────┐     GitHub Actions     ┌─────────────┐
│  Yesterday  │ ──────────────────────> │   Python    │
│   Tracks    │      06:00 UTC daily   │   Script    │
└─────────────┘                         └──────┬──────┘
                                               │
                                               │ Spotify API
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │New Playlist │
                                        │in your      │
                                        │Spotify      │
                                        └─────────────┘
```

**Daily Process:**

1. **6:00 UTC** – GitHub Action triggers automatically
2. **Authenticate** – Using your Refresh Token
3. **Fetch History** – Get tracks played yesterday
4. **Create Playlist** – Generate new playlist with current date
5. **Add Tracks** – Populate playlist with your songs
6. **Done!** – Playlist appears in your Spotify

---

## 📁 Project Structure

```
Daily-Playlist-Generator-for-Spotify/
├── .github/
│   └── workflows/
│       └── playlist.yml           # GitHub Actions workflow
├── generate_playlist.py           # Main script (daily playlists)
├── generate_playlist_six_month.py # 6-month retrospective
├── get_refresh_token.py           # One-time token generator
├── README.md                      # This file
├── README_Advanced.md             # Advanced configuration
└── LICENSE                        # MIT License
```

---

## 🎨 Advanced Usage

### Filter by Mood/Genre

Edit `generate_playlist.py` to add audio feature filtering:

```python
# Get audio features
audio_features = sp.audio_features(track_ids)

# Filter for workout tracks
workout_tracks = [
    track for track, features in zip(tracks, audio_features)
    if features['energy'] > 0.7 and features['tempo'] > 120
]

# Or chill tracks
chill_tracks = [
    track for track, features in zip(tracks, audio_features)
    if features['valence'] > 0.5 and features['energy'] < 0.5
]
```

### Remove Duplicates

```python
# Track unique song IDs
seen_tracks = set()
unique_tracks = []

for track in tracks:
    if track['track']['id'] not in seen_tracks:
        seen_tracks.add(track['track']['id'])
        unique_tracks.append(track)
```

### Add Recommended Songs

```python
# Get recommendations based on your tracks
seed_tracks = [track['track']['id'] for track in tracks[:5]]
recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=20)

# Add to playlist
playlist.extend(recommendations['tracks'])
```

### 6-Month Retrospective

Use the included `generate_playlist_six_month.py` for a quarterly throwback playlist:

```bash
# Manually trigger in GitHub Actions
# or run locally:
python generate_playlist_six_month.py
```

---

## 🧪 Local Testing

Test the script on your machine before deploying:

```bash
# Install dependencies
pip install spotipy

# Set environment variables
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
export SPOTIFY_REFRESH_TOKEN="your_refresh_token"

# Run script
python generate_playlist.py
```

**Expected output:**
```
✅ Authenticated successfully
📅 Fetching tracks from 2026-02-16
🎵 Found 47 tracks played yesterday
📝 Created playlist: Daily Mix - 2026-02-17
✅ Added 47 tracks to playlist
🎉 Done! Check your Spotify account
```

---

## 🐛 Troubleshooting

### Issue: GitHub Action fails with "Invalid token"

**Solution:**
- Regenerate your Refresh Token using `get_refresh_token.py`
- Update the `SPOTIFY_REFRESH_TOKEN` secret in GitHub

### Issue: Empty playlists created

**Solution:**
- Check if you listened to Spotify yesterday
- Verify the date range in the script
- Run locally to see detailed error messages

### Issue: Duplicate playlists

**Solution:**
- The script creates a new playlist every day (by design)
- To avoid duplicates, modify script to check for existing playlists:

```python
# Check if playlist already exists
existing_playlists = sp.current_user_playlists()
for playlist in existing_playlists['items']:
    if playlist['name'] == playlist_name:
        print(f"⚠️ Playlist '{playlist_name}' already exists")
        return
```

### Issue: "Rate limit exceeded"

**Solution:**
- Spotify API has rate limits (429 error)
- Add retry logic with exponential backoff
- Reduce frequency of requests

---

## 📊 Stats & Performance

| Metric | Value |
|--------|-------|
| **Execution Time** | ~5-10 seconds |
| **API Calls** | 3-5 requests per run |
| **GitHub Actions Minutes** | ~1 minute/day (free tier: 2000/month) |
| **Data Usage** | < 1 MB per execution |
| **Spotify Rate Limits** | 100 requests per 30 seconds |

---

## 🔐 Privacy & Security

- ✅ **No Data Storage** – Script only reads Spotify data, never stores it
- ✅ **Secure Tokens** – All credentials stored in GitHub Secrets (encrypted)
- ✅ **Read-Only Access** – Only modifies your own playlists
- ✅ **Open Source** – Full code transparency
- ✅ **No Third-Party** – Direct connection: You ↔ GitHub ↔ Spotify

**What the script can access:**
- ✅ Your recently played tracks (read-only)
- ✅ Your saved playlists (read/write)

**What the script CANNOT access:**
- ❌ Your Spotify password
- ❌ Payment information
- ❌ Private messages
- ❌ Other users' data

---

## 🛣️ Roadmap

- [ ] **Web Dashboard** – View playlist history and statistics
- [ ] **Multi-language Support** – German, Spanish, French documentation
- [ ] **Smart Filtering** – ML-based mood detection
- [ ] **Collaborative Playlists** – Share with friends
- [ ] **Playlist Templates** – Workout, Chill, Focus, Party
- [ ] **Email Notifications** – Get notified when playlist is ready
- [ ] **Apple Music Support** – Expand beyond Spotify

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. ✅ Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎉 Open a Pull Request

**Ideas for contributions:**
- Add support for other streaming services
- Improve playlist algorithms
- Add unit tests
- Create web interface
- Improve documentation

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**TL;DR:** Free to use, modify, and distribute. Just include the original license.

---

## 🙏 Acknowledgments

- [Spotipy](https://github.com/plamere/spotipy) – Spotify Web API wrapper
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) – Official API
- [GitHub Actions](https://github.com/features/actions) – Free automation

---

## 💬 Support

- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/SpeedySwifter/Daily-Playlist-Generator-for-Spotify/issues)
- 💡 **Feature Requests:** [GitHub Discussions](https://github.com/SpeedySwifter/Daily-Playlist-Generator-for-Spotify/discussions)
- 📧 **Email:** sven@hajer.dev
- 🌐 **Website:** [hajer.dev](https://hajer.dev)

---

## ⭐ Show Your Support

If you found this project helpful, please consider:

- ⭐ Starring this repository
- 🍴 Forking and customizing for your needs
- 📢 Sharing with friends who love Spotify
- 🐛 Reporting bugs or suggesting features

---

## 👤 Author

**Sven Hajer**  
Freelance Full-Stack Developer

- GitHub: [@SpeedySwifter](https://github.com/SpeedySwifter)
- Website: [hajer.dev](https://hajer.dev)
- Email: sven@hajer.dev

---

<div align="center">

**Made with ❤️ and 🎵 for music lovers**

[![Stars](https://img.shields.io/github/stars/SpeedySwifter/Daily-Playlist-Generator-for-Spotify?style=social)](https://github.com/SpeedySwifter/Daily-Playlist-Generator-for-Spotify/stargazers)
[![Forks](https://img.shields.io/github/forks/SpeedySwifter/Daily-Playlist-Generator-for-Spotify?style=social)](https://github.com/SpeedySwifter/Daily-Playlist-Generator-for-Spotify/network/members)

**Enjoy your daily soundtrack! 🎧**

</div>
