FROM python:3.11.7

COPY requirements.txt /usr/src/app/

RUN pip3 install -r /usr/src/app/requirements.txt

RUN pip install torch torchvision
RUN pip install --upgrade transformers
RUN pip install mysqlclient


WORKDIR /usr/src/app

COPY . .

# 스크립트 파일 복사
COPY entrypoint.sh /usr/src/app/inglo/

WORKDIR ./inglo

# 스크립트 실행
CMD ["/usr/src/app/inglo/entrypoint.sh"]


EXPOSE 8000