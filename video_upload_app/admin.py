from django.contrib import admin
from .models import Video, Subtitle
# Register your models here.

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['video_file', 'title']

@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ['video', 'language', 'subtitle_file']
