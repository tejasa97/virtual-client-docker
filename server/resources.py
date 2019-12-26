from util import Singleton, list_videos
from settings import IMAGE, HOST_VIDEOS_DIR, CONTAINER_VIDEOS_DIR, MIN_PORT
import docker

class StreamManager(metaclass=Singleton):

    def __init__(self):

        self.__docker_client = docker.from_env()

        self.available_streams = list_videos()
        self.running_streams   = {}

    @property
    def docker_client(self):

        return self.__docker_client

    def get_stream(self, stream_id):
        """Get a stream given its ID
        """

        try:
            return self.running_streams[stream_id]

        except KeyError:
            return None

    def start_stream(self, stream_id):
        """Starts a stream given its ID
        """

        try:
            stream = Stream(self, port=MIN_PORT+stream_id, id=stream_id, name=self.available_streams[stream_id])
        except IndexError:
            print("Stream ID out of bounds")
            return -1

        self.running_streams[stream_id] = stream

    def stop_stream(self, stream_id):
        """Stops a stream given its ID
        """

        del self.running_streams[stream_id]

    def kill_streams(self):
        """Kills all streams
        """

        for stream in self.running_streams.values():
            del stream        

class Stream():

    def __init__(self, stream_manager, port, id, name):

        self.port = port
        self.id   = id
        self.name = name
        self.container = None

        self.start_container(stream_manager)

    def start_container(self, stream_manager):
        """Creates the container and starts streaming
        """

        self.container = stream_manager.docker_client.containers.run(
            image   = IMAGE,
            ports   = {f'{self.port}':self.port},
            volumes = {f'{HOST_VIDEOS_DIR}':{'bind':f'{CONTAINER_VIDEOS_DIR}'}},
            command = f"{self.port} {self.name}",
            detach  = True
        )

    def toJson(self):
        """Serializes the Stream object to JSON
        """

        return {
            'name'         : self.name,
            'port'         : self.port,
            'container_id' : self.container.id
        }

    def __str__(self):

        return f"Container<id={self.container.id}, stream={self.name}, port={self.port}>"

    def __del__(self):

        self.container.kill()
        self.container.remove()