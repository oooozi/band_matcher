from flask import Flask, request, jsonify

app = Flask(__name__)

# 기본 경로 확인용
@app.route('/')
def home():
    return "Flask 서버가 정상 작동 중입니다!"

# 전역 변수: 세션 데이터를 저장하는 딕셔너리
song_sessions = {}


# 프론트로부터 곡별 세션 데이터 받는 엔드포인트
@app.route('/upload_song_sessions', methods=['POST'])
def upload_song_sessions():
    global song_sessions

    # 요청으로부터 JSON 데이터 받기
    data = request.get_json()

    if not data:
        return jsonify({'error': 'JSON 데이터가 없습니다.'}), 400

    # 받은 데이터를 song_sessions에 저장
    song_sessions = data
    print("받은 세션 데이터:", song_sessions)  # 서버 콘솔 출력용

    return jsonify({'status': 'success', 'received': song_sessions}), 200



# 이 파일 실행할 때 Flask 서버 실행하는 코드
if __name__ == '__main__':
    app.run(debug=True)