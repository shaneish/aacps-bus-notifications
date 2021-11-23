FROM python:3.7.12-bullseye

ADD src /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD ["python", "./src/scheduler.py"]