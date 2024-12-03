# Python 3.10 슬림 버전을 사용
FROM python:3.10-slim

# 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# 빌드에 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    libasound2-dev \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# 현재 디렉토리의 모든 파일을 컨테이너의 /app으로 복사
COPY . /app

# PYTHONPATH 환경 변수 설정
ENV PYTHONPATH=/app

# Python 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit 애플리케이션 실행
CMD ["streamlit", "run", "app/app/help_my_exam_main.py", "--server.port=8501", "--server.address=0.0.0.0"]
