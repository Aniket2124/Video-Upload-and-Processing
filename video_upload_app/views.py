from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideoUploadForm
from .models import Video, Subtitle
# from .tasks import process_video

# Create your views here.

def upload_video(request):
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # video = form.save()
            # process_video.delay(video.id)
            return redirect('/videos/')
    else:
        form = VideoUploadForm()
    return render(request, 'video_upload_app/upload_video.html', {'form': form})

def videos_list(request):
    videos = Video.objects.all()
    # videos = Video.objects.filter(processed=True)
    return render(request, 'video_upload_app/videos_list.html', {'videos': videos})


def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    subtitle = Subtitle.objects.get(video=video)
    return render(request, 'video_app/video_detail.html', {'video': video, 'subtitle': subtitle})