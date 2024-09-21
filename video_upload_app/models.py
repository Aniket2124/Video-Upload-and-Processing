from django.db import models

class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    language = models.CharField(max_length=10)  # e.g., 'en', 'es'
    start_time = models.CharField(max_length=20, null=True)
    end_time = models.CharField(max_length=20, null=True)
    subtitle_text = models.TextField(null=True)
    subtitle_file = models.FileField(upload_to='subtitles/', null=True, blank=True)  # To store subtitle files

    def __str__(self) -> str:
        return f"{self.video.title} - {self.language} ({self.start_time} to {self.end_time})"

