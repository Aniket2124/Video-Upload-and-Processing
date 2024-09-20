from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from .models import Video, Subtitle
from django.urls import reverse

class VideoModelTest(TestCase):
    def setUp(self):
        # Create a simple uploaded file for testing
        video_file = SimpleUploadedFile("test_video.mp4", b"video_content", content_type="video/mp4")
        
        # Create a test video instance
        self.video = Video.objects.create(
            video_file=video_file,
            title="Test Video"
        )

    def test_video_creation(self):
        """Test if a video instance is created successfully."""
        self.assertEqual(self.video.title, "Test Video")
        self.assertFalse(self.video.processed)  # By default, processed should be False

    def test_video_string_representation(self):
        """Test the string representation of the video model."""
        self.assertEqual(str(self.video), "Test Video")


class SubtitleModelTest(TestCase):
    def setUp(self):
        # Create a simple uploaded file for testing
        video_file = SimpleUploadedFile("test_video.mp4", b"video_content", content_type="video/mp4")
        
        # Create a test video instance
        self.video = Video.objects.create(
            video_file=video_file,
            title="Test Video"
        )
        
        # Create a test subtitle instance
        self.subtitle = Subtitle.objects.create(
            video=self.video,
            language='en',
            start_time='00:00:05,000',
            end_time='00:00:10,000',
            subtitle_text='Hello, this is a test subtitle.'
        )

    def test_subtitle_creation(self):
        """Test if a subtitle instance is created successfully."""
        self.assertEqual(self.subtitle.language, 'en')
        self.assertEqual(self.subtitle.start_time, '00:00:05,000')
        self.assertEqual(self.subtitle.end_time, '00:00:10,000')
        self.assertEqual(self.subtitle.subtitle_text, 'Hello, this is a test subtitle.')

    def test_subtitle_string_representation(self):
        """Test the string representation of the subtitle model."""
        expected_string = "Test Video - en (00:00:05,000 to 00:00:10,000)"
        self.assertEqual(str(self.subtitle), expected_string)


class UploadVideoViewTest(TestCase):

    def setUp(self):
        # Setup data or other prerequisites here
        self.url = reverse('upload')  # Assuming 'upload' is the name of the URL pattern

    @patch('video_upload_app.views.process_video.delay')  # Mock the Celery task
    def test_upload_video_success(self, mock_process_video):
        """Test if video is uploaded successfully and task is triggered."""
        video_file = SimpleUploadedFile("test_video.mp4", b"video_content", content_type="video/mp4")

        # Simulate a POST request with a valid form
        response = self.client.post(self.url, {
            'title': 'Test Video',
            'video_file': video_file,
        }, follow=True) #after a successful form submission, the user is often redirected to another page

        # Check if video was successfully created
        self.assertEqual(response.status_code, 200)  # Check if the request was successful
        self.assertEqual(Video.objects.count(), 1)  # One video should be created
        video = Video.objects.first()
        self.assertEqual(video.title, 'Test Video')

        # Check if the task was triggered with the correct argument
        mock_process_video.assert_called_once_with(video.id)

        # Ensure it redirects to the videos page (as defined in your view)
        self.assertRedirects(response, '/videos/')

    def test_upload_video_invalid_form(self):
        """Test if invalid form returns the upload page with errors."""
        # Simulate a POST request with an invalid form (missing video file)
        response = self.client.post(self.url, {
            'title': 'Test Video Without File',
        })

        # Check if form is invalid and page renders with errors
        self.assertEqual(response.status_code, 200)  # Form errors should return 200
        # self.assertContains(response, 'This field is required')  # Check error message
        self.assertEqual(Video.objects.count(), 0)  # No video should be created
