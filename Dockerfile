FROM python:3.11.7

COPY requirements.txt /usr/src/app/

RUN pip3 install -r /usr/src/app/requirements.txt

RUN pip install torch torchvision
RUN pip install --upgrade transformers
RUN pip install mysqlclient

WORKDIR /usr/src/app

COPY . .

WORKDIR ./inglo

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000