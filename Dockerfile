FROM python:3.7-alpine

ENV AWS_DEFAULT_REGION=us-east-1

COPY . /opt/alert-table
WORKDIR /opt/alert-table

RUN pip install -r requirements.txt

CMD ./main.py
