import os
import re
from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideoUploadForm
from .models import Video, Subtitle
from .tasks import process_video

# Create your views here.

def upload_video(request):
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            process_video.delay(video.id)
            return redirect('/videos/')
    else:
        form = VideoUploadForm()
    return render(request, 'video_upload_app/upload_video.html', {'form': form})


def videos_list(request):
    videos = Video.objects.filter(processed=True).order_by('-id')
    return render(request, 'video_upload_app/videos_list.html', {'videos': videos})
    

def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    subtitle = Subtitle.objects.filter(video=video).first()  # Assuming one subtitle per video

    subtitle_file_path = None
    search_results = []

    # Check if the subtitle exists and the subtitle file path is valid
    if subtitle and subtitle.subtitle_file:
        subtitle_file_path = subtitle.subtitle_file.path

    if subtitle_file_path and os.path.exists(subtitle_file_path):
        print(f"Subtitle file exists: {subtitle_file_path}")

        # Check for search query in subtitles
        search_query = request.GET.get('q', None)  # e.g., 'search text'
        if search_query:
            search_results = search_in_subtitles(subtitle_file_path, search_query)

    else:
        print("Subtitle file does not exist or path is invalid")

    return render(request, 'video_upload_app/video_detail.html', {
        'video': video,
        'subtitle': subtitle,
        'search_results': search_results,  # Pass search results to template
        'query': search_query,
    })

def search_in_subtitles(subtitle_file_path, search_query):
    """
    Search for the query in the subtitle file and return a list of results with timestamps.
    """
    results = []
    with open(subtitle_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Search the subtitle text for the query
    pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n'
    matches = re.findall(pattern, content, re.DOTALL)

    for start_time, end_time, text in matches:
        if search_query.lower() in text.lower():
            # Format the result with the timestamp and matching text
            results.append({
                'start_time': start_time,
                'end_time': end_time,
                'text': text.strip(),
            })

    return results
