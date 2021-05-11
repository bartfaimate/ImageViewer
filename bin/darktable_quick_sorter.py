#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path
import logging
sys.path.append(Path(__file__).resolve().parents[1].joinpath('lib').as_posix())

from typing import Union, List
import shutil
from datetime import datetime as dt

from darktable.darktable import Darktable
from darktable.constants import basic_xml_fmt

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def parser():
    arg_parser = argparse.ArgumentParser()
    # arg_parser.add_argument('-i', '--inputs', required=True, help="The name of images or numbering of images")
    arg_parser.add_argument('-b', '--base',  required=True, help='The folder where the images are')
    arg_parser.add_argument('-f', '--file', dest='file', help='The text file which contains the numbers of images')
    arg_parser.add_argument('-r', '--rating', dest='rating', help='Rating between 1 and 5', type=int)
    arg_parser.add_argument("-c",'--create',  dest="create", action="store_true", help='Creates XML if does not exist')
    arg_parser.add_argument("-a",'--all',  dest="all", action="store_true", help='Creates XML if does not exist for all image files')


    # arg_parser.add_help()
    return arg_parser


def main():
    args = parser().parse_args()

    base = args.base
    rating = args.rating
    rating = '1' if rating < 1 else str(min(rating, 5))

    file_sort = args.file
    file_sort = Path(file_sort)

    darktable = Darktable(file_numbers=file_sort, base_folder=base)
    if args.all:
        darktable.generate_xmp_for_all()
    else:
        print(rating)
        darktable.change_rating(rating)
        

if __name__ == '__main__':
    main()
