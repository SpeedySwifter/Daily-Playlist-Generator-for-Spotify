# 🎧 Daily Playlist Generator for Spotify

Dieses Projekt erstellt **automatisch jeden Tag eine personalisierte Spotify-Playlist** basierend auf den Songs, die du am Vortag gehört hast. Die Playlist wird direkt in deinem Spotify-Account gespeichert – ideal als täglicher Mix für deinen Start in den Tag ☀️

📦 Automatisiert über **GitHub Actions** – kostenlos, wartungsfrei und täglich aktuell.

---

## 🚀 Features

- Nutzt deine zuletzt gehörten Songs („Recently Played Tracks“)
- Filtert Songs, die **gestern** gespielt wurden
- Erstellt eine Playlist mit aktuellem Datum im Titel
- Tägliche automatische Ausführung über GitHub Actions (6:00 UTC = 8:00 MEZ)
- Playlist wird privat oder öffentlich (je nach Einstellung) in deinem Spotify-Konto gespeichert

---

## 🧰 Voraussetzungen

### 1. Spotify Developer Account & App erstellen

1. Öffne das [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Klicke auf **„Create an App“**
3. Gib z. B. folgende Daten ein:
   - **App Name**: `Daily Playlist Generator`
   - **Redirect URI**:  
     ```
     http://localhost:8888/callback
     ```
4. Notiere dir nach Erstellung:
   - ✅ **Client ID**
   - ✅ **Client Secret**

---

### 2. Refresh Token generieren (einmalig)

Damit GitHub dein Spotify-Konto regelmäßig nutzen darf, brauchst du ein **Refresh Token**. Das wird einmal lokal erzeugt.

#### 🔧 Einmaliges Python-Skript zur Token-Generierung:

```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp_oauth = SpotifyOAuth(
    client_id="DEIN_CLIENT_ID",
    client_secret="DEIN_CLIENT_SECRET",
    redirect_uri="http://localhost:8888/callback",
    scope="user-library-read user-read-recently-played playlist-modify-private playlist-modify-public"
)

token_info = sp_oauth.get_access_token(as_dict=True)
print("Refresh Token:", token_info['refresh_token'])
```

📌 Schritte:
- Ersetze `DEIN_CLIENT_ID` und `DEIN_CLIENT_SECRET` mit deinen Daten
- Installiere vorher `spotipy` mit `pip install spotipy`
- Authentifiziere dich im Browser
- Kopiere den `Refresh Token` aus der Ausgabe

---

## ⚙️ GitHub Setup

### 1. Dieses Repository forken oder klonen

➡ [Zum Repo](https://github.com/SpeedySwifter/Daily-Playlist-Generator-for-Spotify)

### 2. Repository-Secrets einfügen

Gehe zu deinem Repository:

`Settings > Secrets and variables > Actions > New repository secret`

Füge folgende drei Einträge hinzu:

| Name                   | Wert                          |
|------------------------|-------------------------------|
| `SPOTIFY_CLIENT_ID`    | Deine Spotify Client ID       |
| `SPOTIFY_CLIENT_SECRET`| Dein Spotify Client Secret    |
| `SPOTIFY_REFRESH_TOKEN`| Dein generiertes Refresh Token |

---

### 3. GitHub Action aktivieren

Das Projekt enthält bereits die Datei `.github/workflows/playlist.yml`.

- Die Action wird automatisch **täglich um 06:00 UTC** (08:00 MEZ) ausgeführt.
- Oder manuell ausführen: `Actions > Daily Playlist Generator > Run workflow`

---

## ✅ Optional: Skript anpassen

Du kannst das Skript `generate_playlist.py` beliebig erweitern, z. B.:

- Songs nach Genre oder Stimmung filtern (Workout, Chill, Fokus)
- Ähnliche Songs mit `sp.recommendations()` ergänzen
- Dopplungen in Playlists vermeiden
- Mehrtägige History berücksichtigen

---

## 🧪 Lokal testen (optional)

Wenn du das Skript lokal testen willst:

```bash
pip install spotipy
python generate_playlist.py
```

---

## 💬 Feedback oder Ideen?

Gerne als [Issue](https://github.com/SpeedySwifter/Daily-Playlist-Generator-for-Spotify/issues) oder Pull Request.

---

## 📄 Lizenz

[MIT License](LICENSE)

Frei zur privaten und kommerziellen Nutzung – bitte mit Hinweis auf das Originalprojekt.
