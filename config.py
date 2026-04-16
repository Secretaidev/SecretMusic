# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ┃  𝐒𝐄𝐂𝐑𝐄𝐓 𝐌𝐔𝐒𝐈𝐂 𝐁𝐎𝐓 — Proprietary Source Code                     ┃
# ┃  Copyright (c) 2025 𝐒𝐄𝐂𝐑𝐄𝐓 (@its_me_secret)                      ┃
# ┃                                                                    ┃
# ┃  UNAUTHORIZED COPYING OR DISTRIBUTION IS STRICTLY PROHIBITED.     ┃
# ┃  Contact: @its_me_secret | secretfetcher@gmail.com                ┃
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import os
import re
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", None))
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "its_me_secret")
BOT_USERNAME = os.getenv("BOT_USERNAME", "SecretMusicsBot")

MONGO_DB_URI = os.getenv("MONGO_DB_URI", None)
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", None))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")

UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/Secretaidev/SecretMusic")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = os.getenv("GIT_TOKEN", None)

LOGGER_CHANNEL_ID = int(os.getenv("LOGGER_CHANNEL_ID", "-1003968798027"))
PRIVATE_DATA_CHANNEL = int(os.getenv("PRIVATE_DATA_CHANNEL", "-1003797906464"))

SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/secretsbotz")
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "https://t.me/song_assistant")
INSTAGRAM = os.getenv("INSTAGRAM", "https://t.me/its_me_secret")
YOUTUBE = os.getenv("YOUTUBE", "https://t.me/secretsbotz")
GITHUB = os.getenv("GITHUB", "https://github.com/Secretaidev")
DONATE = os.getenv("DONATE", "https://t.me/secretsbotz")
PRIVACY_LINK = os.getenv("PRIVACY_LINK", "https://telegra.ph/SecretMusic-Bot-Privacy-Policy-04-15")

DURATION_LIMIT_MIN = int(os.getenv("DURATION_LIMIT", 300))
PLAYLIST_FETCH_LIMIT = int(os.getenv("PLAYLIST_FETCH_LIMIT", 25))

TG_AUDIO_FILESIZE_LIMIT = int(os.getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(os.getenv("TG_VIDEO_FILESIZE_LIMIT", 2145386496))

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", None)

# ═══════════════════════════════════════════════════════════════
# Download Configuration (v2.1 Upgrades)
# ═══════════════════════════════════════════════════════════════
DOWNLOAD_RETRIES = int(os.getenv("DOWNLOAD_RETRIES", 3))
FRAGMENT_RETRIES = int(os.getenv("FRAGMENT_RETRIES", 2))
DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", 30))
MIN_FILE_SIZE = int(os.getenv("MIN_FILE_SIZE", 500000))  # 500KB - ensure complete files
MAX_AUDIO_BITRATE = int(os.getenv("MAX_AUDIO_BITRATE", 192))  # kbps
PREFERRED_AUDIO_FORMAT = os.getenv("PREFERRED_AUDIO_FORMAT", "mp3")

# Performance Configuration
MAX_CONCURRENT_DOWNLOADS = int(os.getenv("MAX_CONCURRENT_DOWNLOADS", 3))
CACHE_DURATION = int(os.getenv("CACHE_DURATION", 3600))  # 1 hour
DISC_CLEANUP_INTERVAL = int(os.getenv("DISC_CLEANUP_INTERVAL", 21600))  # 6 hours
MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", 5368709120))  # 5GB

# ═══════════════════════════════════════════════════════════════
# YouTube Authentication & Anti-Bot Evasion (v2.1.2+)
# ═══════════════════════════════════════════════════════════════
GVS_PO_TOKEN = os.getenv("GVS_PO_TOKEN", None)  # Extract from https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide
USE_USER_AGENT = os.getenv("USE_USER_AGENT", "true").lower() == "true"
USE_BROWSER_HEADERS = os.getenv("USE_BROWSER_HEADERS", "true").lower() == "true"
RATE_LIMIT_WAIT_BASE = int(os.getenv("RATE_LIMIT_WAIT_BASE", 5))  # seconds
RATE_LIMIT_MAX_BACKOFF = int(os.getenv("RATE_LIMIT_MAX_BACKOFF", 60))  # max wait time
RATE_LIMIT_RETRY_ATTEMPTS = int(os.getenv("RATE_LIMIT_RETRY_ATTEMPTS", 5))

# Feature Flags & Improvements
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
ENABLE_JIOSAAVN_FALLBACK = os.getenv("ENABLE_JIOSAAVN_FALLBACK", "true").lower() == "true"
ENABLE_COOKIE_AUTH = os.getenv("ENABLE_COOKIE_AUTH", "true").lower() == "true"
ENABLE_STATS_TRACKING = os.getenv("ENABLE_STATS_TRACKING", "true").lower() == "true"
AGGRESSIVE_MODE = os.getenv("AGGRESSIVE_MODE", "false").lower() == "true"
AUTO_CLEANUP_DISABLED_FILES = os.getenv("AUTO_CLEANUP_DISABLED_FILES", "true").lower() == "true"
ENABLE_EXPONENTIAL_BACKOFF = os.getenv("ENABLE_EXPONENTIAL_BACKOFF", "true").lower() == "true"

# Logging & Monitoring
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ENABLE_PERFORMANCE_LOGGING = os.getenv("ENABLE_PERFORMANCE_LOGGING", "true").lower() == "true"

STRING1 = os.getenv("STRING_SESSION", None)
STRING2 = os.getenv("STRING_SESSION2", None)
STRING3 = os.getenv("STRING_SESSION3", None)
STRING4 = os.getenv("STRING_SESSION4", None)
STRING5 = os.getenv("STRING_SESSION5", None)

AUTO_LEAVING_ASSISTANT = bool(os.getenv("AUTO_LEAVING_ASSISTANT", False))

START_IMG_URL = os.getenv("START_IMG_URL", "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg")
PING_IMG_URL = "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg"
PLAYLIST_IMG_URL = "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg"
STATS_IMG_URL = "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg"
TELEGRAM_AUDIO_URL = "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg"
TELEGRAM_VIDEO_URL = "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg"
STREAM_IMG_URL = "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg"
SOUNCLOUD_IMG_URL = "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg"
YOUTUBE_IMG_URL = "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://i.ibb.co/vvkm3C0j/IMG-20260415-021910-937.jpg"

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

TEMP_DB_FOLDER = "tempdb"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - SUPPORT_CHANNEL URL is invalid. It must start with https://"
        )

if SUPPORT_GROUP:
    if not re.match(r"(?:http|https)://", SUPPORT_GROUP):
        raise SystemExit(
            "[ERROR] - SUPPORT_GROUP URL is invalid. It must start with https://"
        )
