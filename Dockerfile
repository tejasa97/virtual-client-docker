FROM alpine:latest

# This hack is widely applied to avoid python printing issues in docker containers.
# See: https://github.com/Docker-Hub-frolvlad/docker-alpine-python3/pull/13

ENV PYTHONUNBUFFERED=1
COPY ./script.sh /
VOLUME /videos
WORKDIR /videos

RUN echo "**** install VLC ****"
RUN apk add vlc
RUN adduser -D tejas

RUN chmod +x /script.sh
USER tejas
ENTRYPOINT ["/script.sh"]