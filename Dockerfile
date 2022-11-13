FROM python:3.11.0-alpine3.16

COPY . /

RUN pip install -r requirements.txt

ENTRYPOINT python3 ./bot.py
