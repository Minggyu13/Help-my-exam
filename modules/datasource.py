import os
import base64
from PIL import Image
from io import BytesIO
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
import json

"""
About DATA Process Code

Args:
    openai_api_key : openai api key
    model : openai model name , example : gpt4o
    study_log_json_path : Path of study log json file

"""

class DataSource:
    def __init__(self, openai_api_key, study_log_json_path, chat_and_history_json_path):
        self.openai_key = openai_api_key
        self.study_log_json = study_log_json_path
        self.chat_and_history_json = chat_and_history_json_path
        self.selected_files = list()



    @staticmethod
    def check_vectordb_exists(directory_path='faiss_vector_db'):
        """
           Check if a directory exists.

           Args:
               directory_path (str): Path to the directory.

           Returns:
               bool: True if the directory exists, False otherwise.
           """
        return os.path.isdir(directory_path)





    @staticmethod
    def encode_image_to_base64(image_file_path_list):
        encoded_image_list = list()
        for file_path in image_file_path_list:
            with open(file_path, "rb") as image_file:
                img = Image.open(image_file)
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
                encoded_image_list.append(image_data)


        return encoded_image_list



    @staticmethod
    def chunking_text_splitter(response_list):
        # issue: 청킹이 안됨 TestSplitter에 대해 더 공부하고 원인을 찾아야함
        chunked_text_list = list()
        c_splitter = CharacterTextSplitter(
            chunk_size=30,
            chunk_overlap=0,
            separator='\n\n'
        )

        for response_text in response_list:
            chunked_text = c_splitter.split_text(response_text)
            chunked_text_list.append(chunked_text)


        return chunked_text_list




    def embed_and_add_to_vectorstore(self, chunked_text_list):
        embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=self.openai_key)
        documents_list = list()

        for doc in chunked_text_list:
            documents = [Document(page_content=text) for text in doc]
            documents_list.append(documents)



        if self.check_vectordb_exists():
            vectorstore = FAISS.load_local(
                'faiss_vector_db',
                embedding_model,
                allow_dangerous_deserialization=True
            )
            for data in documents_list:
                vectorstore.add_documents(data)

            vectorstore.save_local('faiss_vector_db')

        else:
            vectorstore = FAISS.from_documents(documents_list[0], embedding_model)
            for data in documents_list[1:]:
                vectorstore.add_documents(data)

            vectorstore.save_local('faiss_vector_db')

    def similarity_search(self,query_text):
        embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=self.openai_key)
        vectorstore = FAISS.load_local(
            'faiss_vector_db',
            embedding_model,
            allow_dangerous_deserialization=True
        )

        searched_texts = vectorstore.similarity_search(query_text, k=3)


        return searched_texts


    @staticmethod
    def load_json_file(path):
        try:
            with open(path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}


    def save_study_log(self, data):
        with open(self.study_log_json, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


    @staticmethod
    def upload_saved_image(directory_path, uploaded_files):
        save_folder = directory_path
        os.makedirs(save_folder, exist_ok=True)

        file_paths = []

        for uploaded_file in uploaded_files:
            # 파일 저장 경로 (절대 경로 포함)
            save_path = os.path.join(os.getcwd(), save_folder, uploaded_file.name)  # 현재 작업 디렉토리 + uploads 폴더

            # 파일을 로컬에 저장
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # 저장된 파일 경로를 리스트에 추가
            file_paths.append(save_path)

        return file_paths

    def save_chat_history(self,conversation_data):

        try:
            with open(self.chat_and_history_json, 'r', encoding="utf-8") as file:
                conversation_history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            conversation_history = []

        # 새로운 대화 추가
        conversation_history.append(conversation_data)

        with open(self.chat_and_history_json, 'w', encoding="utf-8") as file:
            json.dump(conversation_history, file, ensure_ascii=False, indent=4)



