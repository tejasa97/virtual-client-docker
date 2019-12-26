#!/bin/sh

# Get container IP
DOCKER_IP=$(hostname -i)

# Stream the video
PORT="$1"
VIDEO="$2"

echo "Stream : $VIDEO"
echo "Port   : $PORT"

vlc -I dummy $VIDEO --sout "#std{access=http, mux=ts, dst=$DOCKER_IP:$PORT}"