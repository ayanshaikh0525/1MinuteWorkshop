
import os
import tempfile

from utils.video_selector import (
    get_processed_video_for_platform,
    get_random_unprocessed_video
)

from processing.process_video import process_video

from drive.drive_utils import (
    download_file
)

from youtube.generate_metadata import (
    generate_youtube_metadata
)

from youtube.youtube_upload import (
    upload_youtube_video
)

from utils.json_utils import (
    load_videos,
    save_videos
)

PLATFORM = "youtube"


def mark_uploaded(
    video_id,
    upload_id
):
    videos = load_videos()

    for video in videos:

        if video["id"] == video_id:

            video["platforms"]["youtube"] = {
                "uploaded": True,
                "upload_id": upload_id
            }

            break

    save_videos(videos)


def get_video_for_upload():

    # First try processed videos

    video = get_processed_video_for_platform(
        PLATFORM
    )

    if video:
        print("Found processed video")
        return video

    print("No processed video found")

    # Process a new source video

    source_video = get_random_unprocessed_video()

    if not source_video:
        raise Exception(
            "No source videos available"
        )

    process_video(
        source_video
    )

    # Reload json

    video = get_processed_video_for_platform(
        PLATFORM
    )

    if not video:
        raise Exception(
            "Processing failed"
        )

    return video


def main():

    video = get_video_for_upload()

    analysis = video["processed"]["analysis"]

    print("Generating metadata...")

    metadata = generate_youtube_metadata(
        analysis
    )

    with tempfile.TemporaryDirectory() as temp_dir:

        local_video = os.path.join(
            temp_dir,
            "video.mp4"
        )

        print("Downloading processed video...")

        download_file(
            video["processed"]["drive_file_id"],
            local_video
        )

        print("Uploading to YouTube...")

        upload_id = upload_youtube_video(
            video_path=local_video,
            title=metadata["title"],
            description=metadata["description"],
            tags=metadata.get(
                "tags",
                []
            )
        )

    print(
        f"Uploaded successfully: {upload_id}"
    )

    mark_uploaded(
        video["id"],
        upload_id
    )


if __name__ == "__main__":
    main()
