#!/usr/bin/env python3
import unittest
import sys
from pathlib import Path

sys.path.append(Path(__file__).resolve().parents[1].joinpath('lib').as_posix())


from tempfile import TemporaryDirectory, TemporaryFile, tempdir
from unittest.main import main

from darktable.darktable import Darktable


class TestDarktable(unittest.TestCase):
    
    def setUp(self) -> None:
        self.tmpdir = TemporaryDirectory()

        return super().setUp()

    def tearDown(self) -> None:
        self.tmpdir.cleanup()
        return super().tearDown()

    def test_create_xmp(self):
        
        dir_path = Path(self.tmpdir.name) 
        print(dir_path)
        dtable = Darktable(dir_path)
        tmp_img = dir_path.joinpath('dsc002.jpg')
        expect = dir_path.joinpath('dsc002.jpg.xmp')
        dtable.create_xmp(tmp_img)
        # check for creation
        # chek for wrong extensions
        # check for multiple imaes

    

    


if __name__ == '__main__':
    unittest.main(verbosity=2)
    