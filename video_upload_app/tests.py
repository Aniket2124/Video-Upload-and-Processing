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


class VideoViewsTestCase(TestCase):
    def setUp(self):
        # Create a temporary directory for subtitle files
        self.temp_dir = tempfile.mkdtemp()

        # Create a sample video
        self.video = Video.objects.create(
            title='Test Video',
            processed=True,
            video_file='path/to/video.mp4'  # Update this to a valid video path
        )

        # Create a sample subtitle file
        self.subtitle_file = os.path.join(self.temp_dir, 'test_subtitle.srt')
        with open(self.subtitle_file, 'w', encoding='utf-8') as f:
            f.write("1\n00:00:01,000 --> 00:00:02,000\nHello World\n\n")
            f.write("2\n00:00:03,000 --> 00:00:04,000\nGoodbye World\n\n")

        self.subtitle = Subtitle.objects.create(
            video=self.video,
            subtitle_file=self.subtitle_file  # Assuming the model has this field
        )

    def tearDown(self):
        # Clean up the temporary directory
        os.remove(self.subtitle_file)
        os.rmdir(self.temp_dir)

    def test_upload_video_view(self):
        response = self.client.post(reverse('upload_video'), {
            'video_file': open('path/to/video.mp4', 'rb')  # Update to a valid test video file
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after a successful upload
        self.assertTrue(Video.objects.filter(title='Test Video').exists())

    def test_videos_list_view(self):
        response = self.client.get(reverse('videos_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_upload_app/videos_list.html')
        self.assertIn(self.video, response.context['videos'])

    def test_video_detail_view_with_subtitle(self):
        response = self.client.get(reverse('video_detail', args=[self.video.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_upload_app/video_detail.html')
        self.assertEqual(response.context['video'], self.video)
        self.assertIsNotNone(response.context['subtitle'])

    def test_search_in_subtitles(self):
        query = "Hello"
        results = search_in_subtitles(self.subtitle_file, query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['text'], "Hello World")
        self.assertEqual(results[0]['start_time'], "00:00:01,000")

    def test_search_in_subtitles_no_results(self):
        query = "Nonexistent"
        results = search_in_subtitles(self.subtitle_file, query)
        self.assertEqual(len(results), 0)