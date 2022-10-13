FROM python:3.10

MAINTAINER Musfer Adzhymambetov "adzhymambetov@gmail.com"

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt


CMD ["python", "assistant.py"]
