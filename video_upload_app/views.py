from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideoUploadForm, SearchForm
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


# def video_detail(request, video_id):
#     video = get_object_or_404(Video, pk=video_id)
#     subtitle = Subtitle.objects.get(video=video)
#     print(subtitle.start_time,'subtitle------------')
#     print(subtitle.subtitle_text,'subtitle------------')
#     with open(subtitle.subtitle_text, 'r') as file:
#     # Read the contents of the file
#         content = file.read()

# # Print the file contents
#         print(content)
#     search_query = ""
#     print(search_query,'search_query----------------------')
#     timestamp = " "
#     print(timestamp,'timestamp----------------------')
#     if request.method == "POST":
#         print()
#         if "search" in request.POST:
#             search_query = request.POST.get("query")
#             video = Subtitle.objects.filter(video=video, subtitle_text__icontains=search_query)
#             print(video,'video-----------------')
#             # video = Subtitle.objects.filter(subtitle_file__icontains=search_query)
#     if "timestamp" in request.GET:
#         timestamp = request.GET.get("timestamp", 0)
#         print(timestamp,'timestamp----------------------')
#     context = {"video": video, 'subtitle': subtitle, "search_query": search_query, "timestamp": timestamp,}
#     # return render(request, 'video_upload_app/video_detail.html', {'video': video, 'subtitle': subtitle})
#     return render(request, 'video_upload_app/video_detail.html', context)






import os

def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    
    try:
        subtitle = Subtitle.objects.get(video=video)
        subtitle_file_path = subtitle.subtitle_text
        
        # Check if the subtitle file exists before reading
        if os.path.exists(subtitle_file_path):
            with open(subtitle_file_path, 'r') as file:
                content = file.read()
            print(content, 'subtitle file content------------')
        else:
            content = "Subtitles not yet processed or file missing."
            print(content)
    except Subtitle.DoesNotExist:
        content = "Subtitles not available for this video."
        subtitle = None

    search_query = request.POST.get('query', '')  # Search query
    timestamp = request.GET.get('timestamp', '')  # Default timestamp

    subtitle_matches = []
    
    # Handle the search functionality
    if request.method == "POST" and search_query:
        # Case-insensitive search for subtitles
        subtitle_matches = Subtitle.objects.filter(
            video=video,
            subtitle_text__icontains=search_query
        )
        print(subtitle_matches, 'Matching Subtitles')
    
    context = {
        "video": video,
        "subtitle": subtitle,  # Pass subtitle object
        "content": content,  # Pass the subtitle content to the template
        "search_query": search_query,
        "timestamp": timestamp,
        "subtitle_matches": subtitle_matches  # Pass the filtered search results
    }

    return render(request, 'video_upload_app/video_detail.html', context)