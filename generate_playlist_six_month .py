import os
import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Setup Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-library-read user-read-recently-played playlist-modify-private playlist-modify-public"
))

# Zeitgrenzen setzen
today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
six_months_ago = today - datetime.timedelta(days=180)

# Hilfsfunktion: Datetime aus Spotify Zeitstring
def parse_spotify_datetime(date_str):
    return datetime.datetime.strptime(date_str[:19], "%Y-%m-%dT%H:%M:%S")

# 1. Songs vom Vortag sammeln
recent_tracks = sp.current_user_recently_played(limit=50)
yesterday_tracks = [
    item["track"]["uri"]
    for item in recent_tracks["items"]
    if parse_spotify_datetime(item["played_at"]).date() == yesterday.date()
]

# 2. "Liked Songs" der letzten 6 Monate
liked_tracks = []
results = sp.current_user_saved_tracks(limit=50)
while results:
    for item in results["items"]:
        added_at = parse_spotify_datetime(item["added_at"])
        if added_at >= six_months_ago:
            liked_tracks.append(item["track"]["uri"])
    if results["next"]:
        results = sp.next(results)
    else:
        break

# 3. Empfehlungen auf Basis der Tracks von gestern
seed_tracks = yesterday_tracks[:5] if len(yesterday_tracks) >= 1 else liked_tracks[:5]
recommendations = []
if seed_tracks:
    rec = sp.recommendations(seed_tracks=seed_tracks, limit=20)
    recommendations = [track["uri"] for track in rec["tracks"]]

# 4. Playlist zusammenstellen (50% gestern, 30% liked, 20% empfohlen)
total = 30
num_yesterday = min(int(total * 0.5), len(yesterday_tracks))
num_liked = min(int(total * 0.3), len(liked_tracks))
num_recommend = min(int(total * 0.2), len(recommendations))

playlist_tracks = (
    yesterday_tracks[:num_yesterday] +
    liked_tracks[:num_liked] +
    recommendations[:num_recommend]
)

# 5. Playlist erstellen und füllen
if playlist_tracks:
    playlist_name = f"Daily Flow – {today.strftime('%Y-%m-%d')}"
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    sp.playlist_add_items(playlist_id=playlist["id"], items=playlist_tracks)
    print(f"Playlist '{playlist_name}' erstellt mit {len(playlist_tracks)} Songs.")
else:
    print("Keine ausreichenden Daten für Playlist.")