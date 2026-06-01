from utils.json_utils import load_videos
import random


def get_processed_video_for_platform(platform):

    videos = load_videos()

    for video in videos:

        if (
            video["processed"]["exists"]
            and not video["platforms"][platform]["uploaded"]
        ):
            return video

    return None


def get_random_unprocessed_video():

    videos = load_videos()

    candidates = [
        video
        for video in videos
        if not video["processed"]["exists"]
    ]

    if not candidates:
        return None

    return random.choice(candidates)
