import os
import base64
from PIL import Image
from io import BytesIO
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.schema import Document

class DataSource:
    def __init__(self, openai_api_key):
        self.openai_key = openai_api_key
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


    def chatgpt_4o_prompt_template_and_invoke(self, encoded_image_list):
        model = ChatOpenAI(model="gpt-4o", openai_api_key = self.openai_key, temperature=0.3)
        prompt = ChatPromptTemplate.from_messages(
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


        chain = prompt | model
        response_list = list()  # Gpt 4o ocr 후 이미지 글자 처리 데이터 리스트 저장

        for encoded_image in encoded_image_list:
            response = chain.invoke({"image_data": encoded_image})
            response_list.append(response.content)

        return response_list


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

        searched_texts = vectorstore.similarity_search(query_text, k=2)


        return searched_texts
