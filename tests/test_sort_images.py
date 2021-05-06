import shutil
import unittest
from pathlib import Path, PosixPath
from tempfile import TemporaryDirectory, tempdir
import os 
from sort_images import ImageSorter

from distutils.dir_util import copy_tree

LOW = 3984
HIGH = 3994
DIFF = HIGH - LOW
TEST_DIR = Path(__file__).parent.joinpath("test_images")

def generate_files():
    raw_dir = TEST_DIR.joinpath("raw")
    jpeg_dir = TEST_DIR.joinpath("jpeg")
    raw_dir.mkdir(parents=True)
    jpeg_dir.mkdir(parents=True)

    for i in range(LOW-10, HIGH+10):
        with open(jpeg_dir.joinpath(f"DSC0{i}.JPG"), "w") as jpg:
            jpg.write(f"DSC0{i}.JPG")
        with open(raw_dir.joinpath(f"DSC0{i}.RAW"), "w") as raw:
            raw.write(f"DSC0{i}.RAW")

def destroy_files():
    shutil.rmtree(TEST_DIR)

class TestSortImages(unittest.TestCase):

    def setUp(self) -> None:
        generate_files()

    def tearDown(self) -> None:
        destroy_files()

    def test_get_files(self):
        image_sorter = ImageSorter(TEST_DIR)
        files = image_sorter.get_files(TEST_DIR.joinpath("jpeg"))
        raw_files = image_sorter.get_files(TEST_DIR.joinpath("raw"))

        self.assertEqual(len(files), DIFF+20)
        self.assertEqual(len(raw_files), DIFF+20)

        self.assertTrue(list(raw_files)[0][0:3] == "DSC")
        self.assertFalse("RAW" in list(raw_files)[0])


    def test_copy_with_suffix(self):
        """
        copy files with suffix to [dest] from [source] and create [dest] with parents
        """
        image_sorter = ImageSorter(TEST_DIR.joinpath("jpeg"))

        original_len = os.listdir(TEST_DIR.joinpath("jpeg"))
        selected = [f'{str(i)}.JPG' for i in range(LOW, HIGH) ]
        with TemporaryDirectory() as tmp_dir:
            dest = Path(tmp_dir)
            print(dest)
            image_sorter.copy(dest, selected)

            self.assertEqual(DIFF, len(os.listdir(dest)))
            self.assertEqual(original_len, os.listdir(TEST_DIR.joinpath("jpeg")))


    def test_copy_without_suffix(self):
        """
        copy files without suffix to [dest] from [source] and create [dest] with parents
        """
        image_sorter = ImageSorter(TEST_DIR.joinpath("raw"))

        original_len = os.listdir(TEST_DIR.joinpath("raw"))
        selected = [f'{str(i)}' for i in range(LOW, HIGH) ]
        with TemporaryDirectory() as tmp_dir:
            dest = Path(tmp_dir)
            print(dest)
            image_sorter.copy(dest, selected)

            self.assertTrue(DIFF == len(os.listdir(dest)))
            self.assertTrue(original_len == os.listdir(TEST_DIR.joinpath("raw")))

        
    def test_move_with_suffix(self):
        """
        copy xxxx xxxx xxxx contaning files to [dest] from [source] and create [dest] with parents
        xxxx can ends with .jpg or .png or any suffix

        """

        selected = [f'{str(i)}.JPG' for i in range(LOW, HIGH) ]
        with TemporaryDirectory() as secure_dir:
            src = Path(secure_dir)
            copy_tree(TEST_DIR.as_posix(), src.as_posix())
            original_len = os.listdir(src.joinpath("jpeg"))
            image_sorter = ImageSorter(src.joinpath("jpeg"))

            with TemporaryDirectory() as tmp_dir:
                dest = Path(tmp_dir)
                print(dest)
                image_sorter.move(dest, selected)

                self.assertEqual(DIFF, len(os.listdir(dest)))

    def test_move_without_suffix_jpg(self):
        """
        move images given with just numbers to [dest] from [source] fodler and create [dest] with parents
        xxxx can ends with .jpg or .png or any suffix

        """

        selected = [f'{str(i)}' for i in range(LOW, HIGH) ]
        with TemporaryDirectory() as secure_dir:
            src = Path(secure_dir)
            copy_tree(TEST_DIR.as_posix(), src.as_posix())
            original_len = os.listdir(src.joinpath("jpeg"))
            image_sorter = ImageSorter(src.joinpath("jpeg"))

            with TemporaryDirectory() as tmp_dir:
                dest = Path(tmp_dir)
                print(dest)
                image_sorter.move(dest, selected)

                self.assertEqual(DIFF, len(os.listdir(dest)))

    def test_move_without_suffix_raw(self):
        """
        move images given with just numbers to [dest] from [source] fodler and create [dest] with parents
        xxxx can ends with .jpg or .png or any suffix

        """

        selected = [f'{str(i)}' for i in range(LOW, HIGH) ]
        with TemporaryDirectory() as secure_dir:
            src = Path(secure_dir)
            copy_tree(TEST_DIR.as_posix(), src.as_posix())
            original_len = os.listdir(src.joinpath("raw"))
            image_sorter = ImageSorter(src.joinpath("raw"))

            with TemporaryDirectory() as tmp_dir:
                dest = Path(tmp_dir)
                print(dest)
                image_sorter.move(dest, selected)

                self.assertEqual(DIFF, len(os.listdir(dest)))

    def test_delete_with_suffix(self):
        """
        delete files with suffix from [source] 
        """
        selected = [f'{str(i)}.JPG' for i in range(LOW, HIGH) ] # select images
        with TemporaryDirectory() as secure_dir:
            src = Path(secure_dir).joinpath("jpeg")
            copy_tree(TEST_DIR.joinpath("jpeg").as_posix(), src.as_posix()) # copy images to secure them
            original_len = len(os.listdir(src))
            image_sorter = ImageSorter(src)

            image_sorter.delete(selected)

            self.assertEqual(original_len-DIFF, len(os.listdir(src)))

    def test_delete_without_suffix(self):
        """
        delete files without suffix from [source] 
        """
        selected = [f'{str(i)}' for i in range(LOW, HIGH) ] # select images
        with TemporaryDirectory() as secure_dir:
            src = Path(secure_dir).joinpath("raw")
            copy_tree(TEST_DIR.joinpath("raw").as_posix(), src.as_posix()) # copy images to secure them
            original_len = len(os.listdir(src))
            image_sorter = ImageSorter(src)

            image_sorter.delete(selected)

            self.assertEqual(original_len-DIFF, len(os.listdir(src)))

    

if __name__ == "__main__":
    unittest.main(verbosity=2)