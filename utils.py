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

def make_people(person_role: dict, persons_availability: dict) -> list:
    people = []
    
    for name, roles in person_role.items():
        available_time = persons_availability.get(name, [])  # 없으면 빈 리스트
        person = Person(name, roles, available_time)
        people.append(person)
        
    return people



# 공통되는 시간w/가중치 찾기
from collections import defaultdict
def sort_time_list(base_schedule: list, people: list, session_weight: dict) -> list:

    time_list = []

    for time in base_schedule:
        song_info = defaultdict(lambda: {'인원 수': 0, '가중치 합': 0})

        for person in people:
            if time in person.available_time:
                for song, session in person.role:
                    song_info[song]['인원 수'] += 1
                    song_info[song]['가중치 합'] += session_weight.get(session, 0)

        # song_info가 비어 있지 않으면 리스트에 튜플로 추가
        for song, info in song_info.items():
            time_list.append((time, song, info['인원 수'], info['가중치 합']))
    
    # time_list -> (시간, 곡, 인원수, 가중치) 튜플을 저장하는 리스트
    return time_list


# 자동 스케줄링 with 인원 겹침 제거
def assign_schedule(time_list: list, person_role: dict, rooms: int, sort_by="count_first") -> dict:
    schedule = defaultdict(list)  # time -> list of (song, count, weight)
    assigned = set()  # (person, time) 중복 방지용
    
    # 정렬 기준 파라미터 (여러 기준 중 골라서 적용 가능)
    if sort_by == "count_first":
        sort_key = lambda x: (x[0], -x[2], -x[3])  # 시간, 인원수, 가중치 (기본)
    elif sort_by == "weight_first":
        sort_key = lambda x: (x[0], -x[3], -x[2])  # 시간, 가중치, 인원수
    else:
        sort_key = lambda x: (x[0], x[1])  # 시간, 곡 이름순 (방어용: 다른 단어 넣으면 적용됨)

    for time, song, count, weight in sorted(time_list, key=sort_key):
        if len(schedule[time]) >= rooms:
            continue

        conflict = False
        for person, roles in person_role.items():
            for role_song, _ in roles:
                if role_song == song:
                    if (person, time) in assigned:
                        conflict = True
                        break

        if not conflict:
            schedule[time].append((song, count, weight))
            for person, roles in person_role.items():
                for role_song, _ in roles:
                    if role_song == song:
                        assigned.add((person, time))

    return dict(schedule)


# schedule에서 시간별 곡들을 가중치 내림차순으로 정렬
def sort_schedule(schedule: dict) -> dict:
    sorted_schedule = {}

    for time, song_list in schedule.items():
        sorted_list = sorted(song_list, key=lambda x: x[2], reverse=True)
        sorted_schedule[time] = sorted_list

    return sorted_schedule


# 어느 시간에 어떤 곡에 누가 참여하고 불참하는지 return하는 함수
def assign_schedule_participant(
    schedule: dict,
    person_role: dict,
    persons_availability: dict
) -> dict:
    schedule_participant = {}

    for time in sorted(schedule):
        schedule_participant[time] = []

        for song, _, _ in schedule[time]:
            participants = []
            absentees = []

            for person, roles in person_role.items():
                for s, session in roles:
                    if s == song:
                        entry = f"{person}({session})"
                        if time in persons_availability.get(person, []):
                            participants.append(entry)
                        else:
                            absentees.append(entry)

            schedule_participant[time].append({
                song: [participants, absentees] # 리스트[0] -> 참여자, 리스트[1] -> 불참자
            })

    return schedule_participant


# schedule_participant에서, 각 시간당 불참자가 최소인 곡을 배정
# 프론트로 보내서 바로 시각화할 수 있도록 결과 포맷 지정
# 프론트에서는 각 시간마다 곡이 배정된 타임테이블 형식으로 시각화하고,
# 클릭 등을 통해 각 시간마다 참여자/불참자를 확인할 수 있음음
def summarize_for_timetable(schedule_participant: dict) -> dict:
    timetable = {}

    for time, entries in schedule_participant.items():
        best_song = None
        min_absent = float("inf")
        best_pair = [[], []]  # [participants, absentees]

        for entry in entries:
            for song, (participants, absentees) in entry.items():
                if len(absentees) < min_absent:
                    min_absent = len(absentees)
                    best_song = song
                    best_pair = [participants, absentees]

        timetable[time] = (best_song, best_pair)

    return timetable