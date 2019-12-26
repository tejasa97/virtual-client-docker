FROM alpine:latest

# This hack is widely applied to avoid python printing issues in docker containers.
# See: https://github.com/Docker-Hub-frolvlad/docker-alpine-python3/pull/13

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN echo "**** install VLC ****"
RUN adduser -D tejas

RUN echo "**** install Python3 ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

VOLUME /home/saankhyalabs/videos
VOLUME /var/run/docker.sock

EXPOSE 5000

CMD python app.py
