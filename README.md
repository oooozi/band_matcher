# Band Matcher 🎸

밴드 합주를 위한 시간 매칭 웹 서비스입니다.  

---
## 🚀 주요 기능

- 곡별 세션 정보 입력 (보컬, 기타1, 기타2, 드럼 등)
- 멤버별 가능한 시간대 수집
- 공통 가능한 시간대 자동 분석
- 곡별 인원 매칭 결과 시각화

---

## 🔧 설치 방법

```bash
git clone https://github.com/oooozi/band_matcher.git
cd band_matcher
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
---

## 폴더 구조
band_matcher/
├── app.py                 # Flask 웹 서버
├── main.py                # 웹에서 프로그램 실행
├── models.py              # Person 클래스 등 정의
├── utils.py               # 정렬, 매칭 등 유틸 함수
├── data/
│   ├── song_sessions.json
│   ├── persons_availability.json
│   ├── session_weight.json
│   └── base_schedule.json
├── mock_data.py           # JSON 로딩 함수들
└── requirements.txt
