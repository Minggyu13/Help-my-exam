import streamlit as st
import os
import os.path


st.set_page_config(
    page_icon="✨",
    page_title="My data storage",

)


st.title("내 데이터 창고")
# 이미지가 저장된 디렉토리 경로
image_dir = 'uploads'

# 디렉토리 내의 이미지 파일 목록 가져오기
image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]


# 이미지를 삭제할 때 이미지 파일을 삭제하는 함수
def delete_image(image_file):
    try:
        image_path = os.path.join(image_dir, image_file)
        os.remove(image_path)
        st.success(f"{image_file} has been deleted.")
    except Exception as e:
        st.error(f"Error deleting {image_file}: {str(e)}")


# 이미지와 삭제 버튼을 표시
for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)

    # 이미지 표시
    st.image(image_path, caption=image_file, use_container_width=True)

    # 삭제 버튼 만들기
    if st.button(f"Delete {image_file}", key=image_file):
        delete_image(image_file)



