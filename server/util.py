from os import listdir, path
from settings import HOST_VIDEOS_DIR

def list_videos():
    """Returns list of all videos available in the directory
    """

    videos = [f for f in listdir(HOST_VIDEOS_DIR) if path.isfile(path.join(HOST_VIDEOS_DIR, f))]

    return videos

class Singleton(type):
    """
    Define Singleton class for use
    """

    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]