import pyexiv2
from lib.darktable.constants import COLOR_SPACE, FLASH_CODES, ROTATION_CODES

from cached_property import cached_property
from typing import Union
from pathlib import Path


class ImageMetadata:

    def __init__(self, image_path):
        self.image_path = image_path.as_posix() if isinstance(image_path, Path) else Path(image_path).as_posix()
        im = pyexiv2.Image(image_path)
        self.exif = im.read_exif()
        im.close()

    @cached_property
    def image_name(self):
        return Path(self.image_path).name

    @cached_property
    def image_extension(self):
        return Path(self.image_path).suffix
    
    @cached_property
    def orientation(self) -> int:
        orientation = self.exif.get('Exif.Image.Orientation')
        orientation = ROTATION_CODES.get(int(orientation), 0)
        return orientation

    @cached_property
    def image_size(self):
        pass

    @cached_property
    def colorspace(self):
        pass

    @cached_property
    def camera_model(self) -> str:
        return self.exif.get('Exif.Image.Model', 'N/A')

    @cached_property
    def camera_make(self) -> str:
        return self.exif.get('Exif.Image.Make', 'N/A')

    @cached_property
    def iso_speed(self) -> str:
        return self.exif.get('Exif.Photo.ISOSpeedRatings')

    @cached_property
    def flash_mode(self) -> str:
        flash = self.exif.get('Exif.Photo.Flash')
        return FLASH_CODES.get(int(flash))

    @cached_property
    def focal_length(self) -> str:
        focal = self.exif.get('Exif.Photo.FocalLength')
        try:
            num, den = focal.split('/')
        except Exception:
            num, den = focal, 1
        return str(int(num) / int(den))

    @cached_property
    def exposure_time(self) -> str:
        return self.exif.get('Exif.Photo.ExposureTime')

    @cached_property
    def f_number(self) -> str:
        f_number = self.exif.get('Exif.Photo.FNumber')
        try:
            num, den = f_number.split('/')
        except Exception:
            num, den = f_number, 1
        return str(int(num) / int(den))

    @cached_property
    def lens_model(self) -> str:
        return self.exif.get('Exif.Photo.LensModel', 'N/A')