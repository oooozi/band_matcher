from flask import Blueprint, request, jsonify
from .models import *
from .app_db import db
from datetime import datetime

main = Blueprint("main", __name__)

# 관리자: 모임 생성
@main.route("/admin/create", methods=["POST"])
def create_admin_page():
    data = request.get_json()
    title = data["title"]
    songs_sessions = data["songs_sessions"]
    base_schedule = data["base_schedule"]
    session_weight = data.get("session_weight", {})
    rooms = data.get("rooms", 1)

    admin = AdminPage(title=title, rooms=rooms)
    db.session.add(admin)
    db.session.commit()

    for song, sessions in songs_sessions.items():
        for session, name in sessions.items():
            db.session.add(SongSession(admin_id=admin.id, song=song, session=session, name=name))

    for time_str in base_schedule:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        db.session.add(BaseSchedule(admin_id=admin.id, datetime=dt))

    for session, weight in session_weight.items():
        db.session.add(SessionWeight(admin_id=admin.id, session=session, weight=weight))

    db.session.commit()
    return jsonify({"admin_id": admin.id}), 201

# 관리자: 전체 정보 조회
@main.route("/admin/<int:admin_id>", methods=["GET"])
def get_admin_info(admin_id):
    admin = AdminPage.query.get_or_404(admin_id)
    base_schedule = [s.datetime.strftime("%Y-%m-%d %H:%M") for s in admin.base_schedule]
    return jsonify({
        "title": admin.title,
        "rooms": admin.rooms,
        "base_schedule": base_schedule
    }), 200

# 관리자: 참가자 저장 여부만 조회
@main.route("/admin/<int:admin_id>/users", methods=["GET"])
def get_user_status(admin_id):
    persons = PersonAvailability.query.filter_by(admin_id=admin_id).all()
    result = [{"name": p.name, "saved": len(p.times) > 0} for p in persons]
    return jsonify(result), 200

# 관리자: 시간표 생성 결과 보기 (요약만)
@main.route("/admin/<int:admin_id>/schedule", methods=["GET"])
def get_schedule_result(admin_id):
    results = ScheduleParticipant.query.filter_by(admin_id=admin_id).all()
    output = {}
    for r in results:
        time_str = r.datetime.strftime("%Y-%m-%d %H:%M")
        if time_str not in output:
            output[time_str] = []
        output[time_str].append({
            r.song: [[p for p in r.participants], [a for a in r.absentees]]
        })
    return jsonify(output), 200

# 개인: 가능한 시간 저장
@main.route("/user/<int:admin_id>/<string:name>", methods=["POST"])
def save_user_time(admin_id, name):
    data = request.get_json()
    times = data["available_times"]

    existing = PersonAvailability.query.filter_by(admin_id=admin_id, name=name).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()

    person = PersonAvailability(admin_id=admin_id, name=name)
    db.session.add(person)
    db.session.flush()

    for time_str in times:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        db.session.add(AvailableTime(person_id=person.id, datetime=dt))

    db.session.commit()
    return jsonify({"message": "저장 완료"}), 200

# 개인: 시간 조회
@main.route("/user/<int:admin_id>/<string:name>", methods=["GET"])
def get_user_time(admin_id, name):
    person = PersonAvailability.query.filter_by(admin_id=admin_id, name=name).first()
    if not person:
        return jsonify({"available_times": "ALL"})
    times = [t.datetime.strftime("%Y-%m-%d %H:%M") for t in person.times]
    return jsonify({"available_times": times}), 200

# 개인: 시간 수정 (POST와 동일하게 동작)
@main.route("/user/<int:admin_id>/<string:name>", methods=["PUT"])
def update_user_time(admin_id, name):
    return save_user_time(admin_id, name)

# 개인: 시간 초기화
@main.route("/user/<int:admin_id>/<string:name>", methods=["DELETE"])
def reset_user_time(admin_id, name):
    person = PersonAvailability.query.filter_by(admin_id=admin_id, name=name).first()
    if person:
        db.session.delete(person)
        db.session.commit()
    return jsonify({"message": "기본값(모든 시간 가능)으로 초기화됨"}), 200

