FROM arm32v7/python:3.7-slim-bullseye

WORKDIR /usr/src/app

COPY src .
COPY requirements.txt .

RUN apt-get update
RUN apt-get install --yes cron
RUN pip3 install --no-cache-dir --requirement requirements.txt

CMD cron && python ./e-chicken-door.py
