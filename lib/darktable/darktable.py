from argparse import PARSER
from .exceptions import WrongImageFormat
from pathlib import Path
from typing import List, Union, Any
import datetime as dt
import time
from .constants import basic_xml_fmt, EXTENSIONS
import logging

log = logging.getLogger(__name__)


class Darktable:

    def __init__(self,
                 base_folder: Union[Path, str],
                 file_numbers: Union[Path, str] = ''
                 ) -> None:
        if file_numbers:
            self.file_numbers = file_numbers if isinstance(file_numbers, Path) else Path(file_numbers)
        self.base_folder = base_folder if isinstance(base_folder, Path) else Path(base_folder)

    def get_selection_numbers(self) -> List[str]:
        with self.file_numbers.open('r', newline='\n') as fd:
            numbers = fd.read().splitlines()
        return numbers

    def create_xmp(self, image_path: Union[str, Path], rating='1'):
        image_path = image_path if isinstance(image_path, Path) else Path(image_path)

        if not image_path.suffix.lower() in EXTENSIONS:
            raise WrongImageFormat(f'The format for the given image is not supported -- {image_path}')
        if not image_path.is_file():
            raise WrongImageFormat(f'The format for the given image is not supported -- {image_path}')

        xmp_file = Path(str(image_path) + '.xmp')
        if xmp_file.exists():
            return

        derived_from = image_path.name
        creation_time = get_creation_time(image_path)

        log.info(f'Creating {xmp_file}')

        import_timestamp = int(time.time())
        xmp_fd = xmp_file.open('w')
        xmp_fd.write(basic_xml_fmt.format(creation_time, rating, derived_from, import_timestamp))
        xmp_fd.close()

    def modify_rating(self, image_file: Union[Path, str], rating='1'):
        image_file = image_file if isinstance(image_file, Path) else Path(image_file)
        xmp_file = Path(str(image_file) + '.xmp')

        log.info(f'Modifying {xmp_file} to rating={rating}')
        fd = xmp_file.open('r')
        tmp_file = xmp_file.with_suffix('.tmp')
        tmp = tmp_file.open('w')
        for line in fd.readlines():
            if 'xmp:Rating=' in line:
                # print(line)
                new_line = f'{line[:-4]}"{rating}"\n'
                tmp.write(new_line)
            else:
                tmp.write(line)
        tmp.close()
        tmp_file.rename(xmp_file)
        fd.close()
        # tmp_file.unlink()

    def change_rating(self, rating):
        log.info('Change rating')
        for number in self.get_selection_numbers():
            # print(image.stem)
            image_without_suffix = self.base_folder.joinpath(Path(f'DSC{number.zfill(5)}'))

            for suffix in EXTENSIONS:
                image = image_without_suffix.with_suffix(suffix.upper())
                if image.exists():
                    xmp = Path(str(image) + '.xmp')
                    if not xmp.exists():
                        self.create_xmp(image, rating)
                    else:
                        self.modify_rating(image, rating)

    def generate_xmp_for_all(self):
        """
        Generates a basic XMP file for all images in the folder.
        """
        for file in self.base_folder.iterdir():
            if file.is_file() and file.suffix.lower() in EXTENSIONS:
                self.create_xmp(file)


def get_creation_time(image: Path):
    ctime = image.stat().st_ctime
    file_time = dt.datetime.fromtimestamp(ctime)
    creation_time = file_time.strftime("%Y:%m:%d %H:%M:%S")
    return creation_time
