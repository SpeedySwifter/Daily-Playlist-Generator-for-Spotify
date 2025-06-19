import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp_oauth = SpotifyOAuth(
    client_id="DEIN_CLIENT_ID",
    client_secret="DEIN_CLIENT_SECRET",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-library-read user-read-recently-played playlist-modify-private playlist-modify-public"
)

token_info = sp_oauth.get_access_token(as_dict=True)
print("✅ Dein Refresh Token:")
print(token_info["refresh_token"])
