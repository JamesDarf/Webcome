FROM python:3.12

# 환경 변수 설정
ENV port 5000
ENV LOG_FILE_PATH /usr/src/app/logs/app.log

# 애플리케이션 디렉토리 생성 및 이동
WORKDIR /usr/src/app

# 애플리케이션 소스 코드 및 의존성 설치
COPY ./requirements.txt ./
COPY ./main ./
RUN apt-get update 
RUN apt-get install build-essential -y
RUN pip install pyproject.toml
RUN pip install --no-cache-dir -r requirements.txt

# 로그 디렉토리 생성
RUN mkdir logs

# 포트 노출
EXPOSE $port

# 애플리케이션 실행 시 로그 파일을 호스트 머신과 공유하도록 설정
CMD ["python", "./app.py", "2>&1", "|", "tee", "-a", "$LOG_FILE_PATH"]

