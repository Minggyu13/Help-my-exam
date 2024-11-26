import streamlit as st
from datetime import datetime
import json
import os
import shutil
from add_data_source import DataSource
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from openai import OpenAI
from playsound import playsound
from dotenv import load_dotenv


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
data_source = DataSource(openai_api_key)
# JSON 파일 경로 설정
JSON_FILE_PATH = "study_log.json"

st.set_page_config(
    page_icon="✨",
    page_title="Help! my exam",
    layout="wide",

)


# CSS를 통해 버튼 스타일 변경
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: yellow; /* 버튼 배경색 */
        color: black; /* 버튼 텍스트 색 */
        font-size: 18px; /* 폰트 크기 */
        font-weight: bold; /* 텍스트 굵기 */
        border: 0px solid black; /* 테두리 스타일 */
        border-radius: 10px; /* 버튼 둥근 모서리 */
        padding: 10px 20px; /* 버튼 내부 여백 */
        cursor: pointer; /* 마우스 커서 변경 */
    }
    div.stButton > button:hover {
        background-color: gold; /* 호버 시 버튼 색 */
        color: white; /* 호버 시 텍스트 색 */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# 버튼 생성 및 동작


st.title("✨Help! my exam✨")
st.subheader("💛💛💛💛💛💛💛💛💛💛💛💛💛💛💛💛")

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
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

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



test1 = HelpfulAssistiveFunction()

import time
from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st

# 쿠키 관리자 설정
cookies = EncryptedCookieManager(
    prefix="study_session",
    password="your_secure_password_here",  # 고유 비밀번호 설정
)
if not cookies.ready():
    st.stop()  # 쿠키 준비가 안 되면 대기

# 시간 포맷 함수
def format_study_duration(duration_seconds):
    hours = duration_seconds // 3600
    minutes = (duration_seconds % 3600) // 60
    seconds = duration_seconds % 60
    return f"{int(hours)}시간 {int(minutes)}분 {int(seconds)}초"

# 공부 시작 버튼 처리
st.subheader("✨ 순공시간")
col1, col2 = st.columns([1, 10])

with col1:
    if st.button("공부 시작"):
        start_time = time.time()  # 현재 시간 저장
        cookies["start_study_time"] = str(start_time)  # float 값을 문자열로 변환 후 저장
        cookies.save()  # 쿠키 저장
        formatted_time = time.strftime("%p %I시 %M분", time.localtime(start_time))
        formatted_time_korean = formatted_time.replace("AM", "AM").replace("PM", "PN")
        st.text(f"{formatted_time_korean}")

with col2:
    if st.button("공부 끝"):
        end_time = time.time()  # 현재 시간 저장
        cookies["end_study_time"] = str(end_time)  # float 값을 문자열로 변환 후 저장
        cookies.save()  # 쿠키 저장

        # 저장된 시간 가져오기
        start_time = cookies.get("start_study_time", None)
        if start_time:
            start_time = float(start_time)  # 문자열로 저장된 값을 float로 변환
            study_duration_seconds = end_time - start_time
            formatted_study_duration = format_study_duration(study_duration_seconds)
            formatted_end_time = time.strftime("%p %I시 %M분", time.localtime(end_time))
            formatted_end_time_korean = formatted_end_time.replace("AM", "AM").replace("PM", "PM")

            st.text(f"{formatted_end_time_korean}")
            st.text(f"순공: {formatted_study_duration}")
        else:
            st.text("공부 시작 버튼을 먼저 클릭하세요.")


# 오늘의 공부 내용 기록
st.subheader("✨ 오늘의 공부 내용")
note = st.text_input("공부 내용을 입력하세요")

col3, col4 = st.columns([3  , 10])

with col3:
    if st.button("공부 내용 추가 및 업데이트"):
        if note:
            st.session_state.study_notes.append(note)
            st.success(".")
            study_log[today_date] = yesterday_notes + st.session_state.study_notes
            save_study_log(study_log)
            st.success("공부 내용이 추가 및 저장되었습니다.")
        else:
            st.warning("공부 내용을 입력해주세요.")

with col4:
    if st.button("요약 & 피드백 받기"):
        file_path = 'study_log.json'

        # JSON 파일 열기
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 모든 텍스트를 추출하여 조합
        all_texts = []
        for date, entries in data.items():
            all_texts.extend(entries)

        # 조합된 텍스트 출력
        today_study_content_combined_text = ' '.join(all_texts)

        # JSON 파일 경로
        file_path = 'chat_and_response_history.json'

        # JSON 파일 열기
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # user_input과 response를 각각 리스트로 추출
        user_inputs = [entry['user_input'] for entry in data]
        responses = [entry['response'] for entry in data]




        model = ChatOpenAI(model="gpt-4o", openai_api_key=openai_api_key, temperature=0.3)
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "당신은 사용자의 하루 학습 대화와 내용을 요약하고, 교사처럼 건설적이고 격려하는 피드백을 제공하는 챗봇입니다. 사용자의 학습 내용을 분석하여 중요한 점을 강조하고, 개선할 수 있는 부분에 대한 제안을 친절하고 격려하는 어조로 제공합니다."
                ),
                (
                    "user",
                    '''아래는 오늘의 학습 관련 대화와 요약 대상 데이터입니다:

                        1. 사용자와 챗봇 간의 대화 기록:
                        - 사용자가 입력한 내용: {user_inputs}
                        - 챗봇이 제공한 응답: {responses}

                        2. 오늘 공부한 내용 요약:
                        - {today_study_content_combined_text}

                        위 데이터를 바탕으로 다음을 수행하세요:
                        1. 대화 기록에서 중요한 주제를 요약하고, 학습 태도 및 접근 방식에 대한 분석을 제공하세요.
                        2. 오늘 공부한 내용을 바탕으로 중요한 포인트를 요약하세요.
                        3. 사용자가 학습을 더 효과적으로 진행할 수 있도록 구체적이고 실질적인 피드백을 제공하세요.
                        응답은 반드시 한국어로 간결하게 작성하세요.
                    '''
                )
            ]
        )

        # LLMChain 생성
        chain = LLMChain(llm=model, prompt=prompt_template)

        # 데이터 준비
        # 체인 실행

        if "response" not in st.session_state:
            st.session_state.response = ""


        response = chain.run({
            "user_inputs": user_inputs,
            "responses": responses,
            "today_study_content_combined_text": today_study_content_combined_text,
        })

        st.session_state.response = response

        if st.session_state.response:
            st.markdown('<div style="font-family: Arial; font-size: 16px; color: black; font-weight: 500;">',
                    unsafe_allow_html=True)
            st.markdown(st.session_state.response)  # Markdown 렌더링
            st.markdown('</div>', unsafe_allow_html=True)



col8, col9 = st.columns([3  , 10])
with col9:
    if st.button("듣기"):
        def tts_function(input_text):
            client = OpenAI(
                api_key=openai_api_key)

            speech_file_path = "tts_audio.mp3"

            # TTS API 호출
            response = client.audio.speech.create(
                model="tts-1",
                input=input_text,
                voice="alloy",
                response_format="mp3",
                speed=1.1,
            )

            # 음성을 파일로 저장
            response.stream_to_file(speech_file_path)

            # 오디오 재생
            playsound(speech_file_path)


        tts_function(st.session_state.response)
# 어제의 공부 내용 표시
st.subheader("✨ History")
if yesterday_notes:
    for i, y_note in enumerate(yesterday_notes, 1):
        st.write(f"{i}. {y_note}")
else:
    st.write("어제의 공부 내용이 없습니다.")

# 여러 이미지 파일을 선택할 수 있는 파일 업로더
uploaded_files = st.file_uploader("Choose images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# 파일이 업로드되었을 때 처리
if uploaded_files:
    # 저장할 폴더 경로
    save_folder = "uploads"
    os.makedirs(save_folder, exist_ok=True)  # 폴더가 없으면 생성

    # 업로드된 이미지 파일 경로를 저장할 리스트
    file_paths = []

    for uploaded_file in uploaded_files:
        # 파일 저장 경로 (절대 경로 포함)
        save_path = os.path.join(os.getcwd(), save_folder, uploaded_file.name)  # 현재 작업 디렉토리 + uploads 폴더

        # 파일을 로컬에 저장
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 저장된 파일 경로를 리스트에 추가
        file_paths.append(save_path)

    # 저장된 이미지 경로 리스트 출력
    st.write("Files saved at:", file_paths)




col6, col7 = st.columns([3,10])

with col6:
    if st.button("나만의 데이터 창고에 추가하기 "):
        encoded_image_lsit = data_source.encode_image_to_base64(file_paths)
        ocr_image_list = data_source.chatgpt_4o_prompt_template_and_invoke(encoded_image_lsit)
        chunked_list = data_source.chunking_text_splitter(ocr_image_list)
        data_source.embed_and_add_to_vectorstore(chunked_list)
        st.write("나만의 데이터 창고가 만들어졌어요!")



with col7:
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
st.write('''문제가 발생하거나 피드백이 있는 경우 아래의 이메일로 연락을 주세요! 저희는 항상 열려 있습니다!\n
            Email: s23055@gsm.hs.kr 

''')

