import json
from datetime import datetime
from pathlib import Path

# 파일 경로 설정
DATA_DIR = Path(__file__).parent
SONG_SESSIONS_FILE = DATA_DIR / "song_sessions.json"
PERSONS_AVAILABIITY_FILE = DATA_DIR / "persons_availability.json"
BASE_SCHEDULE_FILE = DATA_DIR / "base_schedule.json"
SESSION_WEIGHT_FILE = DATA_DIR / "session_weigjt.json"

# 곡별 세션 정보 불러오기
def load_song_sessions() -> dict:
    with open(SONG_SESSIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 사람별 가능한 시간 불러오기 (문자열 → datetime 변환)
def load_persons_availability() -> dict:
    with open(PERSONS_AVAILABIITY_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
        return {
            name: [datetime.strptime(t, "%Y-%m-%d %H:%M") for t in times]
            for name, times in raw.items()
        }

# 기준 스케줄 불러오기 (문자열 → datetime 변환)
def load_base_schedule() -> list[datetime]:
    with open(BASE_SCHEDULE_FILE, "r", encoding="utf-8") as f:
        times = json.load(f)
        return [datetime.strptime(t, "%Y-%m-%d %H:%M") for t in times]

# 세션별 가중치 불러오기
def load_session_weight() -> dict:
    with open(SESSION_WEIGHT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)