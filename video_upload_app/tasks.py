# from celery import shared_task
# import subprocess
# from .models import Video, Subtitle

# @shared_task
# def process_video(video_id):
#     video = Video.objects.get(id=video_id)
#     video_file_path = video.video_file.path
#     print(video_file_path,'video_file_path-------')
#     # Define the output subtitle file path
  
#     if video_file_path.endswith('.mp4'):
#         subtitle_file_path = video_file_path.replace('.mp4', '.srt')
#     elif video_file_path.endswith('.mkv'):
#         subtitle_file_path = video_file_path.replace('.mkv', '.srt')
#     elif video_file_path.endswith('.webm'):
#         subtitle_file_path = video_file_path.replace('.webm', '.srt')
#     else:
#         print("Unsupported video format")
#         return
#     # subtitle_file_path = video_file_path.replace('.mp4', 'mkv', '.webm', '.srt')
#     print(subtitle_file_path,'subtitle_file_path-----------')

#     # Use FFmpeg to extract subtitles
#     command = f"ffmpeg -i {video_file_path} -map 0:s:0? {subtitle_file_path}"
#     try:
#         # FFmpeg command to extract subtitles into a separate file
#         # command = f"ffmpeg -i {video_file_path} -map 0:s:0 {subtitle_file_path}"
#         subprocess.run(command, shell=True, check=True)
        
#     except subprocess.CalledProcessError as e:
#         print(f"Error extracting subtitles with FFmpeg: {e}")
#         return

#     # Create and save subtitle data in the database
#     Subtitle.objects.create(
#         video=video,
#         language='en',  # Assuming the language is English for now
#         subtitle_text=subtitle_file_path
#     )

#     # Mark the video as processed
#     video.processed = True
#     video.save()






















































import subprocess
import os
from celery import shared_task
from django.conf import settings
from .models import Video, Subtitle

@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)
    video_file_path = video.video_file.path
    print(video_file_path, 'video_file_path-------')

    # Use os.path.splitext to extract the base file name and extension
    video_base, video_extension = os.path.splitext(video_file_path)

    # Define the output subtitle file path based on video extension
    subtitle_file_path = f"{video_base}.srt"
    
    supported_formats = ['.mp4', '.mkv', '.webm']
    if video_extension not in supported_formats:
        print("Unsupported video format:", video_extension)
        return

    print(subtitle_file_path, 'subtitle_file_path-----------')

    # FFmpeg command to extract subtitles
    command = f"ffmpeg -i {video_file_path} -map 0:s:0? {subtitle_file_path}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error extracting subtitles with FFmpeg: {e}")
        return

    # Create and save subtitle data in the database
    Subtitle.objects.create(
        video=video,
        language='en',  # Assuming the language is English for now
        subtitle_text=subtitle_file_path
    )

    # Mark the video as processed
    video.processed = True
    video.save()












# import re
# import os
# from django.conf import settings

# @shared_task
# def process_video(video_id):
#     video = Video.objects.get(uuid=video_id)
#     input_path = os.path.join(settings.MEDIA_ROOT, "uploads", f'video_{video_id}.mp4')
#     output_path = os.path.join(settings.MEDIA_ROOT, "subtitles", f'subtitles_{video_id}.srt')
    
#     # Assuming you're using ccextractor or FFmpeg to extract subtitles
#     ccextractor_command = f'ccextractorwinfull {input_path} -o {output_path}'
#     subprocess.run(ccextractor_command, shell=True)
    
#     # Now open the .srt file and process subtitles
#     with open(output_path, 'r') as subtitle_file:
#         subtitle_text = subtitle_file.read()
#         subtitle_entries = subtitle_text.split('\n\n')
        
#         subtitle_pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")
        
#         for entry in subtitle_entries:
#             lines = entry.split('\n')
#             if len(lines) >= 3:
#                 sequence = lines[0]
#                 time_range = lines[1]
#                 content = '\n'.join(lines[2:]).strip()

#                 # Extract start and end times
#                 match = subtitle_pattern.match(time_range)
#                 if match:
#                     start_time, end_time = match.groups()

#                     # Save each subtitle entry to the database
#                     Subtitle.objects.create(
#                         video=video,
#                         language='en',  # Adjust based on your needs
#                         start_time=start_time,
#                         end_time=end_time,
#                         subtitle_text=content
#                     )
                    
#     video.is_active = True
#     video.save()
#     return "done"


# from celery import shared_task
# import os
# import subprocess
# import re
# from django.conf import settings
# from .models import Video, Subtitle

# from django.core.files import File

# @shared_task
# def process_video(video_id):
#     video = Video.objects.get(id=video_id)
#     video_file_path = video.video_file.path

#     # Define the output subtitle file path in the 'subtitles/' directory
#     subtitles_folder = os.path.join(settings.MEDIA_ROOT, 'subtitles/')
#     if not os.path.exists(subtitles_folder):
#         os.makedirs(subtitles_folder)

#     subtitle_file_path = os.path.join(subtitles_folder, f"{video.title}.srt")

#     # Use FFmpeg to extract subtitles
#     command = f"ffmpeg -i {video_file_path} -map 0:s:0 {subtitle_file_path}"

#     try:
#         subprocess.run(command, shell=True, check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Error extracting subtitles with FFmpeg: {e}")
#         return

#     # Process the extracted subtitle file (.srt)
#     try:
#         with open(subtitle_file_path, 'r', encoding='utf-8') as subtitle_file:
#             subtitle_text = subtitle_file.read()
#             subtitle_entries = subtitle_text.split('\n\n')

#             subtitle_pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")

#             for entry in subtitle_entries:
#                 lines = entry.split('\n')
#                 if len(lines) >= 3:
#                     sequence = lines[0]
#                     time_range = lines[1]
#                     content = '\n'.join(lines[2:]).strip()

#                     # Extract start and end times using regex
#                     match = subtitle_pattern.match(time_range)
#                     if match:
#                         start_time, end_time = match.groups()

#                         # Create Subtitle object and save the subtitle file explicitly
#                         subtitle_instance = Subtitle.objects.create(
#                             video=video,
#                             language='en',  # Adjust based on the subtitle language
#                             start_time=start_time,
#                             end_time=end_time,
#                             subtitle_text=content
#                         )

#                         # Save the subtitle file to the `subtitles/` folder explicitly
#                         with open(subtitle_file_path, 'rb') as srt_file:
#                             subtitle_instance.subtitle_file.save(f"{video.title}.srt", File(srt_file), save=True)

#         # Mark the video as processed
#         video.processed = True
#         video.save()

#     except Exception as e:
#         print(f"Error processing subtitle file: {e}")

#     return "Subtitles extracted and saved successfully."

