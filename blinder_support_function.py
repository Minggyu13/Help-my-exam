import streamlit as st
from openai import OpenAI
from playsound import playsound
import warnings
import os
import speech_recognition as sr



recognizer = sr.Recognizer()

st.button('시각장애인 보조 기능 활성화')

#활성화 했을 때

#어떻게 활성화 시킬까? 버튼으로? 음성으로?


#해제 했을 때




warnings.filterwarnings("ignore", category=DeprecationWarning)
client = OpenAI(api_key="개인 api key")


if st.button('tts'):
    speech_file_path = "tts_audio.mp3"

    # TTS API 호출
    response = client.audio.speech.create(
        model="tts-1",
        input="",
        voice="alloy",
        response_format="mp3",
        speed=1.1,
    )

    # 음성을 파일로 저장
    response.stream_to_file(speech_file_path)

    # 오디오 재생
    playsound(speech_file_path)




if st.button("stt"):
    with sr.Microphone() as source:
        print("말하세요...")
        audio = recognizer.listen(source)

        try:
            print("인식된 텍스트: " + recognizer.recognize_google(audio, language='ko-KR'))
        except sr.UnknownValueError:
            print("Google Web Speech API가 당신의 말을 이해하지 못했습니다.")
        except sr.RequestError as e:
            print(f"Google Web Speech API 서비스에 문제가 발생했습니다; {e}")





# stt와 tts 어떻게 적용할거야 ?
# - 기능을 활성화 하면 일단 챗봇이 말하는거는 다 tts로 들려주고 사용자가 말할때만 노란색 버튼을 누르는 것으로 또한 활성화 되어 있으면 요약 하기 눌렀을때도 말해주고 공부 끝 버튼 눌렀을때도 알려주고


#

# CSS를 통해 버튼 스타일 변경
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: yellow; /* 버튼 배경색 */
        color: black; /* 버튼 텍스트 색 */
        font-size: 18px; /* 폰트 크기 */
        font-weight: bold; /* 텍스트 굵기 */
        border: 2px solid black; /* 테두리 스타일 */
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












st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: yellow; /* 버튼 배경색 */
        color: black; /* 버튼 텍스트 색 */
        font-size: 18px; /* 폰트 크기 */
        font-weight: bold; /* 텍스트 굵기 */
        border: 2px solid black; /* 테두리 스타일 */
        border-radius: 50%; /* 버튼을 동그라미로 */
        padding: 20px; /* 버튼 내부 여백 (균일하게 설정) */
        cursor: pointer; /* 마우스 커서 변경 */
        width: 100px; /* 버튼 너비 */
        height: 100px; /* 버튼 높이 */
        text-align: center; /* 텍스트 가운데 정렬 */
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
if st.button("클릭하세요!"):
    st.write("노란색 버튼을 눌렀습니다!")







