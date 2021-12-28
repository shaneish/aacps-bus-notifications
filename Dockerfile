FROM python:3.8.12-bullseye

ADD requirements.txt /
COPY src /src

RUN pip install -r requirements.txt

CMD ["python", "/src/scheduler.py"]