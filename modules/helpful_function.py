import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import time
from datetime import datetime



class HelpfulAssistiveFunction:

    def __init__(self,cookies, loaded_study_log):
        self.cookies = cookies
        self.study_log = loaded_study_log
        self.today_date = datetime.now().strftime("%Y-%m-%d")
        self.yesterday_notes = self.study_log.get(self.today_date, [])


    def start_study_time(self):
        start_time = time.time()  # 현재 시간 저장
        self.cookies["start_study_time"] = str(start_time)  # float 값을 문자열로 변환 후 저장
        self.cookies.save()  # 쿠키 저장
        formatted_time = time.strftime("%p %I시 %M분", time.localtime(start_time))
        formatted_time_korean = formatted_time.replace("AM", "AM").replace("PM", "PM")

        return formatted_time_korean


    def end_study_time(self):
        end_time = time.time()  # 현재 시간 저장
        self.cookies["end_study_time"] = str(end_time)  # float 값을 문자열로 변환 후 저장
        self.cookies.save()  # 쿠키 저장

        # 저장된 시간 가져오기
        start_time = self.cookies.get("start_study_time", None)
        if start_time:
            start_time = float(start_time)  # 문자열로 저장된 값을 float로 변환
            formatted_end_time = time.strftime("%p %I시 %M분", time.localtime(end_time))
            formatted_end_time_korean = formatted_end_time.replace("AM", "AM").replace("PM", "PM")

            return formatted_end_time_korean

        else:
            return 0



    def format_study_duration(self):
        duration_seconds = float(self.cookies.get("end_study_time", None)) - float(self.cookies.get("start_study_time", None))
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        seconds = duration_seconds % 60
        return f"순공: {int(hours)}시간 {int(minutes)}분 {int(seconds)}초"



    def add_study_note(self, study_note):
        if study_note:
            st.session_state.study_notes.append(study_note)
            self.study_log[self.today_date] = self.yesterday_notes + st.session_state.study_notes








#
#
#
# CSS 설정
# st.markdown(
#     """
#     <style>
#     div.stButton > button {
#         background-color: yellow; /* 버튼 배경색 */
#         color: black; /* 버튼 텍스트 색 */
#         font-size: 18px; /* 폰트 크기 */
#         font-weight: bold; /* 텍스트 굵기 */
#         border: 0px solid black; /* 테두리 스타일 */
#         border-radius: 10px; /* 버튼 둥근 모서리 */
#         padding: 10px 20px; /* 버튼 내부 여백 */
#         cursor: pointer; /* 마우스 커서 변경 */
#     }
#     div.stButton > button:hover {
#         background-color: gold; /* 호버 시 버튼 색 */
#         color: white; /* 호버 시 텍스트 색 */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
