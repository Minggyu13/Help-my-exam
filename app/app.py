import streamlit as st
import time
from datetime import datetime
import json
# JSON 파일 경로 설정
JSON_FILE_PATH = "study_log.json"

st.title("Help! my exam")
if "study_notes" not in st.session_state:
    st.session_state.study_notes = []  # 오늘의 공부 내용 리스트

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



# 순공 시간 기능 :

class HelpfulAssistiveFunction:
    def __init__(self):
        pass

    @staticmethod
    def start_study_time():
        start_time = time.time()
        return start_time

    @staticmethod
    def end_study_time():
        end_time = time.time()
        return end_time


    @staticmethod
    def net_study_time(start_time, end_time):
        # 공부 시작 시각 저장
        start_study_time = start_time

        print("공부 시작 시각:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_study_time)))


        # 공부 종료 시각 저장
        end_study_time = end_time
        print("공부 종료 시각:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_study_time)))




        # 공부 시간 계산
        study_duration = end_time - start_time
        hours = int(study_duration // 3600)
        minutes = int((study_duration % 3600) // 60)
        seconds = int(study_duration % 60)

        print(f"공부 시간: {hours}시간 {minutes}분 {seconds}초")


        return study_duration
    def today_study_content(self):
        pass



test1 = HelpfulAssistiveFunction()


st.subheader("순공시간")
# 버튼 클릭 처리
if st.button("공부 시작"):
    st.session_state.start_study_time = test1.start_study_time()  # 세션 상태에 공부 시작 시간 저장
    st.text("공부 시작 시각: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.session_state.start_study_time)))

if st.button("공부 끝"):
    end_study_time_value = test1.end_study_time()  # 공부 끝 시간을 가져옴
    st.text("공부 종료 시각: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_study_time_value)))

    # 공부 시간 계산
    if 'start_study_time' in st.session_state:
        study_duration = test1.net_study_time(st.session_state.start_study_time, end_study_time_value)
        st.text(f"공부 시간: {study_duration}")
    else:
        st.text("공부 시작 버튼을 먼저 클릭하세요.")


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
st.subheader("공부 내용 History")
if yesterday_notes:
    for i, y_note in enumerate(yesterday_notes, 1):
        st.write(f"{i}. {y_note}")
else:
    st.write("어제의 공부 내용이 없습니다.")
