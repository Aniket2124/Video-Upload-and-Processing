from django.contrib import admin
from .models import Video, Subtitle
# Register your models here.

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_file']

@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ['video', 'language', 'subtitle_text', 'subtitle_file']
