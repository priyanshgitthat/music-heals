
import json
from pathlib import Path
from urllib.parse import quote

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

# =====================================================
# CONFIGURATION
# =====================================================

LANGUAGE = "Hindi"
ID_PREFIX = "HIN"

GITHUB_USERNAME = "priyanshgitthat"
REPO_NAME = "music-heals-hindi"
BRANCH = "main"

SONGS_FOLDER = Path(
    r"E:\Projects\Personal Projects\music-heals-hindi\data"
)

OUTPUT_JSON = Path(
    r"E:\Projects\Personal Projects\music-heals\data\hindi.json"
)

# =====================================================


def safe(tags, key, default="Unknown"):
    return tags.get(key, [default])[0]


# ---------- Load Existing JSON ----------

old_songs = {}

if OUTPUT_JSON.exists():

    with open(OUTPUT_JSON, "r", encoding="utf-8") as f:

        try:

            data = json.load(f)

            for song in data:
                old_songs[song["filename"]] = song

        except Exception:
            pass


# ---------- Find Highest Existing ID ----------

highest = 0

for song in old_songs.values():

    try:
        highest = max(highest, int(song["id"][3:]))
    except:
        pass


songs = []

mp3_files = sorted(SONGS_FOLDER.glob("*.mp3"))

print(f"\nFound {len(mp3_files)} songs\n")


for song in mp3_files:

    tags = EasyID3(song)
    audio = MP3(song)

    duration = int(audio.info.length)

    minutes = duration // 60
    seconds = duration % 60

    encoded = quote(song.name)

    github_url = (
        f"https://raw.githubusercontent.com/"
        f"{GITHUB_USERNAME}/"
        f"{REPO_NAME}/"
        f"{BRANCH}/"
        f"data/{encoded}"
    )

    # ---------- Stable ID ----------

    if song.name in old_songs:

        song_id = old_songs[song.name]["id"]

    else:

        highest += 1

        song_id = f"{ID_PREFIX}{highest:04d}"

    title = safe(tags, "title", song.stem)
    artist = safe(tags, "artist")
    album = safe(tags, "album")
    year = safe(tags, "date")
    genre = safe(tags, "genre")

    search = (
        f"{title} {artist} {album} {LANGUAGE}"
    ).lower()

    songs.append({

        "id": song_id,

        "title": title,

        "artist": artist,

        "album": album,

        "language": LANGUAGE,

        "year": year,

        "genre": genre,

        "duration": f"{minutes}:{seconds:02}",

        "filename": song.name,

        "url": github_url,

        "cover": "",

        "search": search

    })

    print(f"✓ {title}")

# ---------- Sort By Title ----------

songs.sort(key=lambda x: x["title"].lower())

# ---------- Save ----------

OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:

    json.dump(
        songs,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\n--------------------------------")
print("JSON Generated Successfully")
print("--------------------------------")
