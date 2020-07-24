FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /news_board_API

COPY . /news_board_API
RUN pip install -r /news_board_API/req.txt