from django import forms
from .models import Video, Subtitle

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_file', 'title']