import tempfile
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings


class UploadFileTests(TestCase):
    def test_completed_upload_is_saved_and_returns_created(self):
        """A fully received file must get a 201 response, not a server error."""
        with tempfile.TemporaryDirectory() as temporary_dir:
            media_root = Path(temporary_dir) / 'media'
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    '/upload/',
                    {'file': SimpleUploadedFile('test.txt', b'complete upload')},
                )

                self.assertEqual(response.status_code, 201)
                self.assertTrue((media_root / 'test.txt').is_file())

    def test_download_preserves_the_original_filename_and_content_type(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            media_root = Path(temporary_dir) / 'media'
            upload_dir = media_root
            upload_dir.mkdir(parents=True)
            (upload_dir / 'report.pdf').write_bytes(b'%PDF-test')

            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.get('/download/report.pdf/')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/pdf')
            self.assertIn('report.pdf', response['Content-Disposition'])
            self.assertEqual(b''.join(response.streaming_content), b'%PDF-test')

    def test_download_rejects_paths_outside_the_upload_directory(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            media_root = Path(temporary_dir) / 'media'
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.get('/download/..%2Fsecret.txt/')

            self.assertEqual(response.status_code, 404)
