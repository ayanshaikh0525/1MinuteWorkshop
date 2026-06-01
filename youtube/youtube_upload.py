
import os

from google.oauth2.credentials import Credentials

from googleapiclient.discovery import build

from googleapiclient.http import MediaFileUpload


TOKEN_FILE = "auth/token.json"


def get_youtube_service():

    credentials = Credentials.from_authorized_user_file(
        TOKEN_FILE,
        [
            "https://www.googleapis.com/auth/youtube.upload"
        ]
    )

    return build(
        "youtube",
        "v3",
        credentials=credentials
    )
