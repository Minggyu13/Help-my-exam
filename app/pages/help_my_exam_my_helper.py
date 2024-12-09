from datetime import datetime
import streamlit as st
from modules.datasource import DataSource
import os
from llm.custom_llm import CustomLLMService
from modules.assistive_features import AssistiveFeatures
from dotenv import load_dotenv

openai_api_key = os.getenv("OPENAI_API_KEY")
data_source = DataSource(openai_api_key,study_log_json_path="data/study_log.json", chat_and_history_json_path="data/chat_and_history.json")
assistive_features = AssistiveFeatures(openai_api_key=openai_api_key)
custom_llm_service = CustomLLMService(openai_api_key= openai_api_key, model="gpt-4o")
study_log = data_source.load_json_file(data_source.study_log_json)
load_dotenv()



# 페이지 아이콘 , 페이지 이름 설정
st.set_page_config(
    page_icon="✨",
    page_title="My Helper",
)



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

    # 세션 상태 초기화
if "tts_check" not in st.session_state:
    st.session_state.tts_check = False

if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""  # 초기값 설정



col1, col2 = st.columns([1,0.1])

with col1:
    if st.button("말하기"):
        stt_user_input = assistive_features.stt_service()
        if stt_user_input:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 사용자 메시지 저장 및 표시
            st.session_state.messages.append({"role": "user", "content": stt_user_input})
            with st.chat_message("user"):
                st.write(stt_user_input)

            # 검색 결과 가져오기
            with st.spinner("Searching for relevant information..."):
                retrieved_docs = data_source.similarity_search(stt_user_input)
                retrieved_texts = "\n".join(doc.page_content for doc in retrieved_docs)


            # 검색된 내용을 사이드바에 표시
            with st.sidebar:
                st.header("🔍 검색된 정보")
                st.write(retrieved_texts)

            # 모델 응답 생성
            with st.chat_message("assistant"):
                with st.spinner("Generating response..."):
                    ai_response = custom_llm_service.rag_chatbot(stt_user_input=stt_user_input, retrieved_texts=retrieved_texts,)
                    st.write(ai_response)

            # 응답 저장
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

            conversation_data = {
                "date": current_time,
                "user_input": stt_user_input,
                "response": ai_response
            }

            st.session_state.ai_response = ai_response
            data_source.save_chat_history(conversation_data)


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
            ai_response = custom_llm_service.rag_chatbot(stt_user_input=user_input, retrieved_texts=retrieved_texts)
            st.write(ai_response)


        # 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    conversation_data = {
        "date": current_time,
        "user_input": user_input,
        "response": ai_response
    }

    st.session_state.ai_response = ai_response
    data_source.save_chat_history(conversation_data)

with col2:
    if st.button("듣기"):
        assistive_features.tts_service(st.session_state.ai_response)

