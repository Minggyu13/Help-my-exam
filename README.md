# Help-my-exam
시각장애인을 위한 보조 기능과 RAG(Relevant Answer Generation) 기반 고등학교 과목별 시험 대비 학습 챗봇과 일주일동안 공부한 점 ai 요약 서비스, 각종 시험에 도움되는 기능을 포함한 웹 서비스


## How to run?
### docker build -t help_my_exam:latest . 
### docker run -p 8000:8000 help_my_exam uvicorn main:app --host 0.0.0.0 --port 8000 --reload

