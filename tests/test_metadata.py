import unittest
from images.metadata import ImageMetadata

from pathlib import Path
import sys

sys.path.append(Path(__file__).resolve().parents[1].joinpath('lib').as_posix())

RAW_PATH_90 = Path(__file__).resolve().parents[1].joinpath('etc/images/raw/DSC03984.ARW')
RAW_PATH = Path(__file__).resolve().parents[1].joinpath('etc/images/raw/DSC08326.ARW')
JPEG_PATH_90 = Path(__file__).resolve().parents[1].joinpath('etc/images/jpeg/DSC03984.JPG')
JPEG_PATH = Path(__file__).resolve().parents[1].joinpath('etc/images/jpeg/DSC08326.JPG')


class TestMetadata(unittest.TestCase):

    def test_construct(self):
        metadata_raw = ImageMetadata(RAW_PATH_90)
        metadata_jpg = ImageMetadata(JPEG_PATH_90)

    def test_orientation_raw(self):
        metadata_raw_90 = ImageMetadata(RAW_PATH_90)
        self.assertEqual(metadata_raw_90.orientation, 90)

        metadata_raw = ImageMetadata(RAW_PATH)
        self.assertEqual(metadata_raw.orientation, 0)

    def test_orientation_jpg(self):
        metadata_90 = ImageMetadata(JPEG_PATH_90)
        self.assertEqual(metadata_90.orientation, 90)

        metadata = ImageMetadata(JPEG_PATH)
        self.assertEqual(metadata.orientation, 0)

    def test_camera_model_and_make(self):
        metadata = ImageMetadata(RAW_PATH)
        self.assertEqual(metadata.camera_make.lower(), 'sony')
        self.assertEqual(metadata.camera_model.lower(), 'ilce-7m2')

        metadata = ImageMetadata(JPEG_PATH)
        self.assertEqual(metadata.camera_make.lower(), 'sony')
        self.assertEqual(metadata.camera_model.lower(), 'ilce-7m2')

    def test_iso_speed(self):
        metadata = ImageMetadata(RAW_PATH_90)
        self.assertEqual(metadata.iso_speed, '1250')

        metadata = ImageMetadata(RAW_PATH)
        self.assertEqual(metadata.iso_speed, '100')

        metadata = ImageMetadata(JPEG_PATH_90)
        self.assertEqual(metadata.iso_speed, '1250')

        metadata = ImageMetadata(JPEG_PATH)
        self.assertEqual(metadata.iso_speed, '100')

    def test_f_number(self):
        metadata = ImageMetadata(RAW_PATH_90)
        self.assertEqual(metadata.f_number, '5.6')

        metadata = ImageMetadata(RAW_PATH)
        self.assertEqual(metadata.f_number, '1.8')

        metadata = ImageMetadata(JPEG_PATH_90)
        self.assertEqual(metadata.f_number, '5.6')

        metadata = ImageMetadata(JPEG_PATH)
        self.assertEqual(metadata.f_number, '1.8')

    def test_shutter(self):
        metadata = ImageMetadata(JPEG_PATH)
        self.assertEqual(metadata.exposure_time, '1/2500')

        metadata = ImageMetadata(JPEG_PATH_90)
        self.assertEqual(metadata.exposure_time, '1/20')

        metadata = ImageMetadata(RAW_PATH)
        self.assertEqual(metadata.exposure_time, '1/2500')

        metadata = ImageMetadata(RAW_PATH_90)
        self.assertEqual(metadata.exposure_time, '1/20')


if __name__ == '__main__':
    unittest.main(verbosity=2)