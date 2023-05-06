FROM python:alpine

WORKDIR /telegrambot

COPY bot bot
COPY db db
COPY main.py main.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
