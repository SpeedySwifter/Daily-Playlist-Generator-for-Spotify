import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="DEINE_CLIENT_ID",
    client_secret="DEIN_CLIENT_SECRET",
    redirect_uri="http://127.0.0.1:8888/callback"
    scope="user-library-read user-read-recently-played playlist-modify-private playlist-modify-public"
))

# 1. Songs von gestern holen
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
recent_tracks = sp.current_user_recently_played(limit=50)

yesterday_tracks = [
    item["track"]["uri"]
    for item in recent_tracks["items"]
    if datetime.datetime.strptime(item["played_at"][:19], "%Y-%m-%dT%H:%M:%S").date() == yesterday.date()
]

# 2. Playlist erstellen
today_str = datetime.datetime.now().strftime("%Y-%m-%d")
playlist_name = f"Daily Mix – {today_str}"

user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)

# 3. Songs hinzufügen
if yesterday_tracks:
    sp.playlist_add_items(playlist_id=playlist["id"], items=yesterday_tracks)
else:
    print("Keine Songs von gestern gefunden.")