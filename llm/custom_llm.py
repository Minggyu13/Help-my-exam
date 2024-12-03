from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory


class CustomLLMService:
    def __init__(self, openai_api_key, model):
        self.openai_api_key = openai_api_key
        self.model = model


    def summary_llm_service(self, study_log_data,chat_and_response_history_data):
        all_texts = []

        for date, entries in study_log_data.items():
            all_texts.extend(entries)

        today_study_content_combined_text = ' '.join(all_texts)

        # user_input과 response를 각각 리스트로 추출
        user_inputs = [entry['user_input'] for entry in chat_and_response_history_data]
        responses = [entry['response'] for entry in chat_and_response_history_data]


        model = ChatOpenAI(model=self.model, openai_api_key=self.openai_api_key, temperature=0.3)
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

        chain = LLMChain(llm=model, prompt=prompt_template)

        response = chain.run({
            "user_inputs": user_inputs,
            "responses": responses,
            "today_study_content_combined_text": today_study_content_combined_text,
        })

        return response


    def ocr_image_llm_service(self, encoded_image_list):
        model = ChatOpenAI(model= self.model, openai_api_key = self.openai_api_key, temperature=0.3)
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", """Avoid including introductory phrases such as "This document is" or "This is a document about." Please transform the following table data into a natural and consistent narrative format. Do not preserve the table structure, but instead, explain the meaning of each entry clearly in sentence form. Be sure to accurately express the relationships between the different entries, so that the search system can understand each concept correctly. Focus on turning the table’s structure into coherent and clear sentences without losing any of the information contained in the table. For example, for entries like 'person,' 'argument,' or 'model,' connect them naturally into a sentence and emphasize the key points. Ensure that the main concepts are well-explained and clearly articulated, to avoid confusion when searching for similar queries in the future.Additionally, set the minimum chunk length to 300 characters. Ensure that each chunk maintains a coherent flow and avoids being too short. This will help preserve the context and improve the quality of downstream processing tasks. If the chunk exceeds the minimum length, keep it continuous without unnecessary splitting. Answer in KOREAN."""),
                (
                    "user",
                    [
                        {
                            "type": "image_url",
                            "image_url": {"url": "data:image/jpeg;base64,{image_data}"},
                        }
                    ],
                ),
            ]
        )

        chain = prompt_template | model
        response_list = list()

        for encoded_image in encoded_image_list:
            response = chain.invoke({"image_data": encoded_image})
            response_list.append(response.content)

        return response_list



    def rag_chatbot(self, stt_user_input, retrieved_texts):
        model = ChatOpenAI(model=self.model, openai_api_key = self.openai_api_key, temperature=0.3)
        memory = ConversationBufferWindowMemory(memory_key="chat_history", k=3, input_key="question")
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an AI assistant having a conversation with a human. Use the information below to answer their question"

                ),
                (
                    "user",
                    """You are an AI assistant having a conversation with a human. Use the information below to answer their question:
            
                                Relevant information:
                                {retrieved_docs}
            
                                Chat history:
                                {chat_history}
            
                                Human: {question}
                                AI:"""

                )
            ]
        )

        chain = LLMChain(llm=model, memory=memory, prompt=prompt_template)

        ai_response = chain.predict(
            question=stt_user_input,
            retrieved_docs=retrieved_texts
        )



        return ai_response

