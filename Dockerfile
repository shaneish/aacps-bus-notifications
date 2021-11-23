FROM python:3.7.12-bullseye

ADD requirements.txt /
COPY src /src

RUN pip install -r requirements.txt

CMD ["python", "/src/scheduler.py"]