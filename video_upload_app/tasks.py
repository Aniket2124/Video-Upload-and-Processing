from celery import shared_task
import os
import subprocess
from .models import Video, Subtitle

@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)
    video_file_path = video.video_file.path

    # Define the output subtitle file path based on video format
    if video_file_path.endswith('.mp4'):
        subtitle_file_path = video_file_path.replace('.mp4', '.srt')
    elif video_file_path.endswith('.mkv'):
        subtitle_file_path = video_file_path.replace('.mkv', '.srt')
    elif video_file_path.endswith('.webm'):
        subtitle_file_path = video_file_path.replace('.webm', '.srt')
    else:
        print("Unsupported video format")
        return

    try:
        command = f"ffmpeg -i {video_file_path} -map 0:s:0? {subtitle_file_path}"
        subprocess.run(command, shell=True, check=True)

        # Check if the subtitle file is created
        if os.path.exists(subtitle_file_path):
            # Save the subtitle file to the database
            Subtitle.objects.create(
                video=video,
                language='en',
                subtitle_file=subtitle_file_path 
            )
        else:
            print("Subtitle file creation failed")

        # Mark the video as processed
        video.processed = True
        video.save()

    except subprocess.CalledProcessError as e:
        print(f"Error extracting subtitles with FFmpeg: {e}")