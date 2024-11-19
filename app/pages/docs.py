import streamlit as st
import time
import json
from datetime import datetime

# JSON 파일 경로 설정
JSON_FILE_PATH = "study_log.json"

# 초기화: 세션 상태 및 파일
if "time_value" not in st.session_state:
    st.session_state.time_value = 0  # 순공시간 초기값
if "study_notes" not in st.session_state:
    st.session_state.study_notes = []  # 오늘의 공부 내용 리스트
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False  # 타이머 실행 상태

# JSON 파일 읽기 함수
def load_study_log():
    try:
        with open(JSON_FILE_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# JSON 파일 쓰기 함수
def save_study_log(data):
    with open(JSON_FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

# 어제의 공부 내용 불러오기
study_log = load_study_log()
today_date = datetime.now().strftime("%Y-%m-%d")
yesterday_notes = study_log.get(today_date, [])

st.title("순공시간 & 공부 내용 기록")

# 타이머 컨트롤
timer_placeholder = st.empty()
if st.button("타이머 시작"):
    st.session_state.timer_running = True

if st.button("타이머 종료"):
    st.session_state.timer_running = False

# 타이머가 실행 중일 때 시간 증가 및 업데이트
if st.session_state.timer_running:
    start_time = time.time()
    while st.session_state.timer_running:
        elapsed_time = int(time.time() - start_time)
        st.session_state.time_value += elapsed_time
        timer_placeholder.metric(label="순공시간 (초)", value=st.session_state.time_value)
        time.sleep(1)

# 오늘의 공부 내용 기록
st.subheader("오늘의 공부 내용")
note = st.text_input("공부 내용을 입력하세요")
if st.button("공부 내용 추가"):
    if note:
        st.session_state.study_notes.append(note)
        st.success("공부 내용이 추가되었습니다.")
    else:
        st.warning("공부 내용을 입력해주세요.")

# 저장 버튼: JSON 파일에 저장
if st.button("업데이트"):
    study_log[today_date] = yesterday_notes + st.session_state.study_notes
    save_study_log(study_log)
    st.success("공부 내용이 저장되었습니다.")

# 어제의 공부 내용 표시
st.subheader("어제의 공부 내용")
if yesterday_notes:
    for i, y_note in enumerate(yesterday_notes, 1):
        st.write(f"{i}. {y_note}")
else:
    st.write("어제의 공부 내용이 없습니다.")
