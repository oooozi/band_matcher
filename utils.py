# sons_sessions(곡별 세션 정보)를 person_role(이름별 역할)로 정리한 딕셔너리 반환
def make_person_role(song_sessions: dict) -> dict:
    
    person_role = {}
    for song, sessions in song_sessions.items():
        for session, name in sessions.items():
            if name is None:
                continue
            if name not in person_role:
                person_role[name] = []
            person_role[name].append((song, session))
    return person_role


# Person 객체를 people 리스트에 저장
from models import Person

def make_people(person_role: dict) -> list:
    people = []
    
    for name, _ in person_role.items():
        if name not in people:
            people.append(Person(name))
    return people



# 공통되는 시간w/가중치 찾기
from collections import defaultdict
def sort_time_list(base_schedule: list, people: list, session_weight: dict) -> list:

    result = []

    for time in base_schedule:
        song_info = defaultdict(lambda: {'인원 수': 0, '가중치 합': 0})

        for person in people:
            if time in person.available_time:
                for song, session in person.role:
                    song_info[song]['인원 수'] += 1
                    song_info[song]['가중치 합'] += session_weight.get(session, 0)

        # song_info가 비어 있지 않으면 리스트에 튜플로 추가
        for song, info in song_info.items():
            result.append((time, song, info['인원 수'], info['가중치 합']))
    
    # result -> (시간, 곡, 인원수, 가중치) 튜플을 저장하는 리스트
    return result


# 자동 스케줄링 with 인원 겹침 제거

def assign_schedule(time_list: list, person_role: dict, rooms: int) -> dict:
    schedule = defaultdict(list)  # time -> list of (song, count, weight)
    assigned = set()  # (person, time) 중복 방지용

    for time, song, count, weight in sorted(time_list, key=lambda x: (x[0], -x[3])):
        if len(schedule[time]) >= rooms:
            continue

        conflict = False
        for person, roles in person_role.items():
            if (song, _) in roles:
                if (person, time) in assigned:
                    conflict = True
                    break

        if not conflict:
            schedule[time].append((song, count, weight))
            for person, roles in person_role.items():
                if (song, _) in roles:
                    assigned.add((person, time))

    return dict(schedule)