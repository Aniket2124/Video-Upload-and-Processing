from django import forms
from .models import Video, Subtitle

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_file', 'title']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, label="Search Subtitles")