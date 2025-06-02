from flask import Flask, render_template, request, jsonify
from utils import (
    make_person_role,
    make_people,
    sort_time_list,
    assign_schedule,
    assign_schedule_participant,
)
from datetime import datetime
import os
from backend import create_app


app = create_app()


# 기본 경로 확인용
@app.route('/')
def home():
    return "Flask 서버가 정상 작동 중입니다!"

# mock data 테스트용 플래그 (True면 mock_data로 실행됨)
USE_MOCK = os.getenv("USE_MOCK", "False") == "True"

if USE_MOCK:
    from mock_data import load_mock_case
    
    data = load_mock_case("case1")
    song_sessions = data["song_sessions"]
    persons_availability = data["persons_availability"]
    base_schedule = data["base_schedule"]
    session_weight = data["session_weight"]


@app.route("/process", methods=["POST"])
def process_schedule():
    try:
        # 실제 요청 or mock data 분기
        if USE_MOCK:
            from mock_data import load_mock_case
    
            data = load_mock_case("case1")
            song_sessions = data["song_sessions"]
            persons_availability = data["persons_availability"]
            base_schedule = data["base_schedule"]
            session_weight = data["session_weight"]
            rooms = 3
        else:
            data = request.get_json()
            song_sessions = data["song_sessions"]
            persons_availability = data["persons_availability"]
            base_schedule = data["base_schedule"]
            session_weight = data["session_weight"]
            rooms = data["rooms"]
        
        # song_sessions → person_role로 변환
        person_role = make_person_role(song_sessions)
        
        # people 리스트에 Person 객체 저장
        people = make_people(person_role, persons_availability)
        
        # 시간당 곡, 참여자, 가중치 튜플 리스트 반환
        time_list = sort_time_list(base_schedule, people, session_weight)
         
        # 자동 스케줄링
        schedule = assign_schedule(time_list, person_role, rooms=rooms)

        # 참여/불참자 매핑
        participant_info = assign_schedule_participant(schedule, person_role, persons_availability)

        # datetime key → 문자열 변환
        result = {
            time.strftime("%Y-%m-%d %H:%M") if hasattr(time, "strftime") else str(time): value
            for time, value in participant_info.items()
        }

        return jsonify({
            "rooms": rooms,
            "schedule": {
                time.strftime("%Y-%m-%d %H:%M") if hasattr(time, "strftime") else str(time): value
                for time, value in participant_info.items()
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/web")
def web_view():
    return render_template("index.html")



# 이 파일 실행할 때 Flask 서버 실행하는 코드
if __name__ == '__main__':
    app.run(debug=True)