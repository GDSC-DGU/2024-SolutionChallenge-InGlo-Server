FROM python:3.11.7

# 필요한 패키지 설치, cron 추가
RUN apt-get update && apt-get install -y cron

COPY requirements.txt /usr/src/app/

RUN pip3 install -r /usr/src/app/requirements.txt

RUN pip install torch torchvision
RUN pip install --upgrade transformers
RUN pip install mysqlclient
RUN pip install aioboto3


WORKDIR /usr/src/app

COPY . .

# 스크립트 파일 및 cronjob 파일 복사
COPY entrypoint.sh /usr/src/app/inglo/
COPY cronjob /etc/cron.d/my-cron-job

# cronjob 파일 권한 설정, 로그 파일 준비 및 cron 작업 활성화
RUN chmod 0644 /etc/cron.d/my-cron-job \
    && touch /var/log/cron.log \
    && crontab /etc/cron.d/my-cron-job

WORKDIR ./inglo

# 스크립트 실행 권한 부여 및 스크립트 실행
RUN chmod +x /usr/src/app/inglo/entrypoint.sh
CMD ["/usr/src/app/inglo/entrypoint.sh"]

EXPOSE 8000