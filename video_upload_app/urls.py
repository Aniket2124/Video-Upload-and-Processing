from django.urls import path, include
from video_upload_app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.upload_video, name='upload'),
    path('videos/', views.videos_list, name='video_list'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)