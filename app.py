from flask import Flask, request, jsonify

app = Flask(__name__)

# 기본 경로 확인용
@app.route('/')
def home():
    return "Flask 서버가 정상 작동 중입니다!"


# mock_data를 불러와서 전역변수로 저장
# 백엔드 로직 확인 후 -> 전역변수 없애고, 프론트로부터 POST받아 저장하는는 코드 작성해야 함
from mock_data import (
    load_song_sessions,
    load_persons_availability,
    load_base_schedule,
    load_session_weight
)

song_sessions = load_song_sessions()
persons_availability = load_persons_availability()
base_schedule = load_base_schedule()
session_weight = load_session_weight()

# 방 개수를 전역변수로 저장
rooms = 3


# 이 파일 실행할 때 Flask 서버 실행하는 코드
if __name__ == '__main__':
    app.run(debug=True)