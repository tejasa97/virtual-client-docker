from flask import Flask, jsonify, Response, abort, request
from resources import StreamManager
import json

stream_manager = StreamManager()
app = Flask(__name__)

@app.route('/listVideos', methods=['GET'])
def listVideos():

    videos = stream_manager.available_streams

    return Response(json.dumps(
        {
            "videos" : videos
        }
    ), mimetype="application/json"
    )

@app.route('/startStream', methods=['POST'])
def startStream():

    data     = json.loads(request.data)
    video_id = data.get('id', None)

    if video_id is None:
        abort(400, "Required data not provided")

    existing_stream = stream_manager.get_stream(video_id)
    if existing_stream:
        abort(400, f"Stream with ID {video_id} already running")

    stream_manager.start_stream(video_id)

    return jsonify(
        {"status" : "started"}
    )

@app.route('/stopStream', methods=['POST'])
def stopStream():

    data     = json.loads(request.data)
    video_id = data.get('id', None)

    if video_id is None:
        abort(400, "Required data not provided")

    if stream_manager.get_stream(video_id) is None:
        abort(400, f'No stream with ID {video_id} found')

    stream_manager.stop_stream(video_id)

    return jsonify(
        {"status" : "stopped"}
    )

@app.route('/runningStreams', methods=['GET'])
def runningStreams():

    return Response(json.dumps(
        {
        "runningStreams" : stream_manager.running_streams
        }, default=lambda x:x.toJson()
    ), mimetype="application/json"
    )

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
