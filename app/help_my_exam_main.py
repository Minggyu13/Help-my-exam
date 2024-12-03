import streamlit as st
import os
import shutil
from modules.datasource import DataSource
from llm.custom_llm import CustomLLMService
from modules.helpful_function import HelpfulAssistiveFunction
from streamlit_cookies_manager import EncryptedCookieManager
from modules.assistive_features import AssistiveFeatures
from dotenv import load_dotenv

#
# """
#
# Clean Code Refactoring
#
# 리팩토링 시작
# DATE : 2024/12/2
#
#
# Author : 강민규
#
# """



st.set_page_config(
    page_icon="✨",
    page_title="Help! my exam",
    layout="wide",
)

st.title("✨Help! my exam✨")
st.subheader("💛💛💛💛💛💛💛💛💛💛💛💛💛💛💛💛")


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
data_source = DataSource(openai_api_key, study_log_json_path="data/study_log.json", chat_and_history_json_path="data/chat_and_history.json")
assistive_features = AssistiveFeatures(openai_api_key=openai_api_key)
custom_llm_service = CustomLLMService(openai_api_key= openai_api_key, model="gpt-4o")
study_log = data_source.load_json_file(data_source.study_log_json)
# 쿠키 관리자 설정
cookies = EncryptedCookieManager(
    prefix="study_session",
    password="your_secure_password_here",  # 고유 비밀번호 설정
)


if not cookies.ready():
    st.stop()  # 쿠키 준비가 안 되면 대기

helpful_function = HelpfulAssistiveFunction(loaded_study_log = study_log, cookies=cookies)
today_date = helpful_function.today_date
yesterday_notes = study_log.get(today_date, [])



st.subheader("✨ 순공시간")
col1, col2 = st.columns([1, 10])

with col1:
    if st.button("공부 시작"):
        formatted_start_time_korean = helpful_function.start_study_time()

        st.text(f"{formatted_start_time_korean}")

with col2:
    if st.button("공부 끝"):
        formatted_end_time_korean = helpful_function.end_study_time()
        if formatted_end_time_korean[0]:
            formatted_study_duration = helpful_function.format_study_duration()

            st.text(f"{formatted_end_time_korean}")
            st.text(f"{formatted_study_duration}")

        else:
            st.text("공부 시작 버튼을 먼저 클릭하세요.")


st.subheader("✨ 오늘의 공부 내용")
study_note = st.text_input("공부 내용을 입력하세요")
col3, col4 = st.columns([3,10])


if "study_notes" not in st.session_state:
    st.session_state.study_notes = []



with col3:
    if st.button("공부 내용 추가 및 업데이트"):
        if study_note:
            helpful_function.add_study_note(study_note)
            data_source.save_study_log(study_log)
            st.success("공부 내용이 추가 및 저장되었습니다.")
        else:
            st.warning("공부 내용을 입력해주세요.")

with col4:
    if st.button("요약 & 피드백 받기"):
        study_log_data = data_source.load_json_file(data_source.study_log_json)
        chat_and_response_history_data = data_source.load_json_file(data_source.chat_and_history_json)

        if "response" not in st.session_state:
            st.session_state.response = str()

        response = custom_llm_service.summary_llm_service(study_log_data = study_log_data, chat_and_response_history_data=chat_and_response_history_data,)
        st.session_state.response = response

        if st.session_state.response:
            st.markdown('<div style="font-family: Arial; font-size: 16px; color: black; font-weight: 500;">',
                    unsafe_allow_html=True)
            st.markdown(st.session_state.response)  # Markdown 렌더링
            st.markdown('</div>', unsafe_allow_html=True)



col5, col6 = st.columns([3  , 10])
with col5:
    if st.button("듣기"):
        assistive_features.tts_service(st.session_state.response)


# 어제의 공부 내용 표시
st.subheader("✨ History")
if yesterday_notes:
    for i, y_note in enumerate(yesterday_notes, 1):
        st.write(f"{i}. {y_note}")
else:
    st.write("어제의 공부 내용이 없습니다.")

st.write("")
st.subheader("💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗")
# 여러 이미지 파일을 선택할 수 있는 파일 업로더
uploaded_files = st.file_uploader("Choose images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# 파일이 업로드되었을 때 처리
if uploaded_files:
    file_paths = data_source.upload_saved_image(uploaded_files=uploaded_files, directory_path="uploads")

col7, col8 = st.columns([3,10])

with col7:
    if st.button("나만의 데이터 창고에 추가하기 "):
        encoded_image_lsit = data_source.encode_image_to_base64(file_paths)
        ocr_image_list = custom_llm_service.ocr_image_llm_service(encoded_image_lsit)
        chunked_list = data_source.chunking_text_splitter(ocr_image_list)
        data_source.embed_and_add_to_vectorstore(chunked_list)
        st.write("나만의 데이터 창고가 만들어졌어요!")



with col8:
    if st.button("나만의 데이터 창고 삭제하기"):
        dir_name = "vector_db"

        if not os.path.exists(dir_name):
            print(f"디렉터리 '{dir_name}'이(가) 존재하지 않습니다.")


        try:
            shutil.rmtree(dir_name)  # 비어 있지 않아도 삭제 가능
            print(f"디렉터리 '{dir_name}'이(가) 성공적으로 삭제되었습니다.")
        except Exception as e:
            print(f"디렉터리 삭제 중 오류 발생: {e}")
            st.write("데이터 창고가 삭제되었습니다.")


# 피드백, 문의함 기능
st.text("")
st.write('''
문제가 발생하거나 피드백이 있는 경우 아래의 이메일로 연락을 주세요!\n
            Email: s23055@gsm.hs.kr
''')

