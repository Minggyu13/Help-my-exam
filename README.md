# Help-my-exam
시각장애인을 위한 보조 기능과 RAG(Retrieval-Augmented Generation) 기반 고등학교 과목별 시험 대비 학습 챗봇과 일주일동안 공부한 점 ai 요약 서비스, 각종 시험에 도움되는 기능을 포함한 웹 서비스


## OS : Ubuntu 22.04 LTS

## How to run?
### docker build -t help_my_exam:latest . 
### docker run help_my_exam

## If you want to run it on your local computer

### 1. sudo apt update && sudo apt install portaudio19-dev
### 2. export PYTHONPATH="your_path/Help-my-exam"
### 3. streamlit run app/help_my_exam_main.py
