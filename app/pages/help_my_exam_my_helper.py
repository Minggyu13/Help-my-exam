import json
from datetime import datetime
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from add_data_source import DataSource
import os
import speech_recognition as sr
from openai import OpenAI
from playsound import playsound
from dotenv import load_dotenv



load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
json_file_path = 'chat_and_response_history.json'



def save_to_json(data):
    # 기존에 파일이 있으면 내용 읽고 새 대화 추가, 없으면 새 파일 생성
    try:
        with open(json_file_path, 'r', encoding="utf-8") as file:
            conversation_history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        conversation_history = []


    # 새로운 대화 추가
    conversation_history.append(data)

    with open(json_file_path, 'w', encoding="utf-8") as file:
        json.dump(conversation_history, file, ensure_ascii=False, indent=4)


recognizer = sr.Recognizer()

# 페이지 아이콘 , 페이지 이름 설정
st.set_page_config(
    page_icon="✨",
    page_title="My Helper",
)

# OpenAI API 키 설정

# 데이터 소스 초기화
data_source = DataSource(openai_api_key)

# 프롬프트 템플릿
prompt = PromptTemplate(
    input_variables=["chat_history", "question", "retrieved_docs"],
    template="""You are an AI assistant having a conversation with a human. Use the information below to answer their question:

    Relevant information:
    {retrieved_docs}

    Chat history:
    {chat_history}

    Human: {question}
    AI:"""
)

# 모델 및 메모리 설정
llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
memory = ConversationBufferWindowMemory(memory_key="chat_history", k=3, input_key="question")
llm_chain = LLMChain(llm=llm, memory=memory, prompt=prompt)

# Streamlit UI 설정
st.title("✨Help! my exam✨")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "궁금한 내용을 물어보세요!"}
    ]

# 이전 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])




st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: yellow; /* 버튼 배경색 */
        color: black; /* 버튼 텍스트 색 */
        font-size: 18px; /* 폰트 크기 */
        font-weight: bold; /* 텍스트 굵기 */
        border: 0px solid black; /* 테두리 스타일 */
        border-radius: 50%; /* 버튼을 동그라미로 */
        padding: 20px; /* 버튼 내부 여백 (균일하게 설정) */
        cursor: pointer; /* 마우스 커서 변경 */
        width: 100px; /* 버튼 너비 */
        height: 100px; /* 버튼 높이 */
        text-align: center; /* 텍스트 가운데 정렬 */
    }
    div.stButton > button:hover {
        background-color: yellow; /* 호버 시 버튼 색 */
        color: white; /* 호버 시 텍스트 색 */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def tts_function(input_text):
    client = OpenAI(
        api_key=openai_api_key
    )

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
col1, col2 = st.columns([1,5])

with col1:
    # 버튼 생성 및 동작
    if st.button("말하기"):
        # with sr.Microphone() as source:
        #     print("듣고 있습니다!")
        #     audio = recognizer.listen(source)

            try:
                # print("인식된 텍스트: " + recognizer.recognize_google(audio, language='ko-KR'))
                # user_input = recognizer.recognize_google(audio, language='ko-KR')
                user_input = "갑신정변이 뭐야?"



                if user_input:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # 사용자 메시지 저장 및 표시
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    with st.chat_message("user"):
                        st.write(user_input)

                    # 검색 결과 가져오기
                    with st.spinner("Searching for relevant information..."):
                        retrieved_docs = data_source.similarity_search(user_input)
                        retrieved_texts = "\n".join(doc.page_content for doc in retrieved_docs)
                        print(retrieved_texts)

                    # 검색된 내용을 사이드바에 표시
                    with st.sidebar:
                        st.header("🔍 검색된 정보")
                        st.write(retrieved_texts)

                    # 모델 응답 생성
                    with st.chat_message("assistant"):
                        with st.spinner("Generating response..."):
                            ai_response = llm_chain.predict(
                                question=user_input,
                                retrieved_docs=retrieved_texts
                            )
                            st.write(ai_response)

                    # 응답 저장
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})

                    conversation_data = {
                        "date": current_time,
                        "user_input": user_input,
                        "response": ai_response
                    }
                    save_to_json(conversation_data)


            except sr.UnknownValueError:
                print("Google Web Speech API가 당신의 말을 이해하지 못했습니다.")
            except sr.RequestError as e:
                print(f"Google Web Speech API 서비스에 문제가 발생했습니다; {e}")


# 사용자 입력 받기
user_input = st.chat_input()

if user_input:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 사용자 메시지 저장 및 표시
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    #0 검색 결과 가져오기
    with st.spinner("Searching for relevant information..."):
        retrieved_docs = data_source.similarity_search(user_input)
        retrieved_texts = "\n".join(doc.page_content for doc in retrieved_docs)
        print(retrieved_texts)

        # 검색된 내용을 사이드바에 표시
    with st.sidebar:
        st.header("🔍 검색된 정보")
        st.write(retrieved_texts)

    # 모델 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            ai_response = llm_chain.predict(
                question=user_input,
                retrieved_docs=retrieved_texts
                )
            st.write(ai_response)

            if st.session_state.tts_check:
                tts_function(ai_response)

        # 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    conversation_data = {
        "date": current_time,
        "user_input": user_input,
        "response": ai_response
    }
    save_to_json(conversation_data)


with col2:
    # 세션 상태 초기화
    if "tts_check" not in st.session_state:
        st.session_state.tts_check = False

    if st.button("듣기"):
        # 현재 상태를 반대로 전환
        st.session_state.tts_check = not st.session_state.tts_check
        st.write(st.session_state.tts_check)


