import logging
from pathlib import Path
from typing import Union
import rawpy
from PIL import Image as PImage

log = logging.getLogger(__name__)

from metadata import ImageMetadata

class Image():

    def __init__(self, image_path: Union[Path, str]):
        self.image_path = image_path.as_posix() if isinstance(image_path, Path) else Path(image_path).as_posix()
        self.meta = ImageMetadata(self.image_path)