import json
from datetime import datetime
from pathlib import Path

import json
from datetime import datetime
from pathlib import Path


#mock_data/{case_name}/ 하위의 4가지 JSON을 한 번에 불러오는 함수
def load_mock_case(case_name: str) -> dict:
    base_path = Path(__file__).parent / "mock_data" / case_name

    with open(base_path / "song_sessions.json", encoding="utf-8") as f:
        song_sessions = json.load(f)

    with open(base_path / "persons_availability.json", encoding="utf-8") as f:
        persons_availability = {
            name: [datetime.strptime(t, "%Y-%m-%d %H:%M") for t in times]
            for name, times in json.load(f).items()
        }

    with open(base_path / "base_schedule.json", encoding="utf-8") as f:
        base_schedule = [datetime.strptime(t, "%Y-%m-%d %H:%M") for t in json.load(f)]

    with open(base_path / "session_weight.json", encoding="utf-8") as f:
        session_weight = json.load(f)

    return {
        "song_sessions": song_sessions,
        "persons_availability": persons_availability,
        "base_schedule": base_schedule,
        "session_weight": session_weight,
    }


