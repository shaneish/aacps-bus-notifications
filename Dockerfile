FROM python:3.8.12-bullseye

ADD requirements.txt /
ADD docker_deploy.sh /
COPY src /src

RUN pip install -r requirements.txt

CMD ["./docker_deploy.sh"]