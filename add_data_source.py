import os
import base64
from PIL import Image
from io import BytesIO
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
import warnings

# input open ai api key
api_key = ""



# image를 fileloading으로 선택 했을 때 image_data에 추가하는 메서드 필요






def get_image_file_paths(directory):
    # 이미지 파일 확장자 목록
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

    # 디렉토리 내의 이미지 파일 경로를 저장할 리스트
    image_files = []

    # 디렉토리 내의 모든 파일을 검사
    for filename in os.listdir(directory):
        # 파일의 전체 경로를 생성
        file_path = os.path.join(directory, filename)

        # 파일이 디렉토리가 아닌 경우에만 처리
        if os.path.isfile(file_path):
            # 파일의 확장자를 확인
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                image_files.append(file_path)

    return image_files


# 사용 예시
directory_path = 'image_data'
image_file_paths = get_image_file_paths(directory_path)


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        img = Image.open(image_file)
        img = img.resize((1000, 1000))
        buffer = BytesIO()
        img.save(buffer, format="PNG")

        return base64.b64encode(buffer.getvalue()).decode("utf-8")


# PDF 요소에서 이미지 경로를 가져옴
encoded_image_list = list()

for path in image_file_paths:
    image_data = encode_image_to_base64(path)
    encoded_image_list.append(image_data)






from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", openai_api_key = api_key, temperature=0.3)
model2 = ChatOpenAI(model="gpt-4o-mini", openai_api_key = api_key, temperature=0.4)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Avoid including introductory phrases such as 'This document is' or 'This is a document about. Please transform the following table data into a natural and consistent narrative format. Do not preserve the table structure, but instead, explain the meaning of each entry clearly in sentence form. Be sure to accurately express the relationships between the different entries, so that the search system can understand each concept correctly. Focus on turning the table’s structure into coherent and clear sentences without losing any of the information contained in the table. Avoid maintaining the table format, and instead, prioritize converting the information into a descriptive format. For example, for entries like 'person,' 'argument,' or 'model,' connect them naturally into a sentence and emphasize the key points. Ensure that the main concepts are well-explained and clearly articulated, to avoid confusion when searching for similar queries in the future. Answer in KOREAN."),
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


response_list = list()

for image_data in encoded_image_list:
    response = chain.invoke({"image_data": image_data})
    response_list.append(response.content)

chunked_text_list = list()

c_splitter = CharacterTextSplitter(
    chunk_size=30,
    chunk_overlap=0,
    separator='\n\n'
)

for response_text in response_list:
    chunked_text = c_splitter.split_text(response_text)
    chunked_text_list.append(chunked_text)





