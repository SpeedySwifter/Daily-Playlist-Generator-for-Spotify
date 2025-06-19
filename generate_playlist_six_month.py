import os
import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# Setup Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read user-read-recently-played playlist-modify-private playlist-modify-public"
))

def parse_spotify_datetime(date_str):
    return datetime.datetime.strptime(date_str[:19], "%Y-%m-%dT%H:%M:%S")

# Zeitfenster definieren
today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
six_months_ago = today - datetime.timedelta(days=180)

print("🔄 Tracks von gestern sammeln...")
recent_tracks = sp.current_user_recently_played(limit=50)
yesterday_tracks = [
    item["track"]["uri"]
    for item in recent_tracks["items"]
    if parse_spotify_datetime(item["played_at"]).date() == yesterday.date()
]
print(f"➡️ {len(yesterday_tracks)} Tracks von gestern gefunden")

# Liked Songs der letzten 6 Monate sammeln
print("🔄 Liked Tracks der letzten 6 Monate sammeln...")
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
print(f"➡️ {len(liked_tracks)} liked Tracks gefunden")

# Empfehlungen vorbereiten mit gültigen Seed-IDs
def extract_track_id(uri):
    return uri.split(":")[-1] if ":" in uri else uri

def is_valid_seed(track_id):
    try:
        track = sp.track(track_id)
        return True
    except:
        return False

seed_candidates = yesterday_tracks if yesterday_tracks else liked_tracks
raw_seed_ids = [extract_track_id(uri) for uri in seed_candidates if uri]
filtered_seed_ids = [sid for sid in raw_seed_ids if is_valid_seed(sid)]

seed_tracks = filtered_seed_ids[:5]
print("🎯 Verwendbare Seed-IDs:", seed_tracks)

recommendations = []
if seed_tracks:
    try:
        rec = sp.recommendations(seed_tracks=seed_tracks, limit=20)
        recommendations = [track["uri"] for track in rec["tracks"]]
        print(f"➡️ {len(recommendations)} Empfehlungen erhalten")
    except Exception as e:
        print("❌ Fehler bei Empfehlungen:", e)

# Playlist-Zusammenstellung
total = 30
num_yesterday = min(int(total * 0.5), len(yesterday_tracks))
num_liked = min(int(total * 0.3), len(liked_tracks))
num_recommend = min(int(total * 0.2), len(recommendations))

playlist_tracks = (
    yesterday_tracks[:num_yesterday] +
    liked_tracks[:num_liked] +
    recommendations[:num_recommend]
)

# Fallback bei fehlenden Empfehlungen
if num_recommend == 0:
    needed = total - len(playlist_tracks)
    fallback = liked_tracks[num_liked:num_liked + needed]
    playlist_tracks += fallback
    print(f"⚠️ Empfehlungen fehlen – {len(fallback)} weitere liked Tracks als Ersatz verwendet")

# Playlist erstellen
if playlist_tracks:
    playlist_name = f"Daily Flow – {today.strftime('%Y-%m-%d')}"
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    sp.playlist_add_items(playlist_id=playlist["id"], items=playlist_tracks)
    print(f"✅ Playlist '{playlist_name}' erstellt mit {len(playlist_tracks)} Songs.")
else:
    print("⚠️ Keine geeigneten Songs gefunden. Playlist nicht erstellt.")