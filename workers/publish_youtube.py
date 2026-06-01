processed_video = get_processed_video_for_platform(
    "youtube"
)

if processed_video:

    publish(processed_video)

else:

    source_video = get_random_unprocessed_video()

    processed_video = process_video(
        source_video
    )

    publish(processed_video)
