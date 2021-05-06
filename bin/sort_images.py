#! /usr/bin/python3

import os
import sys
import argparse
from pathlib import Path
from typing import Union, List
import shutil

# get the filenames without extension
# get parent of files (jpeg)
# get the sibling folder(raw)
# get differencfrom the raw stem-s and the jpg-stems

class ImageSorter:

    def __init__(self, base_path:Union[str, Path], input_list : List[str]=None, dry_run=False):
        self.base_path = Path(base_path) if isinstance(base_path, str) else base_path
        self._input_list = input_list
        self.dry_run = dry_run


    def set_input_list(self, input_list):
        self._input_list = input_list

    def delete(self, input_list: List[str]):
        prefix = "[DRY_RUN] Would delete" if self.dry_run else "Deleting"
        for selected in self.select_files(input_list):
            print(f"{prefix} {selected}")
            if not self.dry_run:
                selected.unlink()
    
    def prepare_dir(self, directory:Union[str, Path]):
        directory = Path(directory) if isinstance(directory, str) else directory

        if not directory.is_dir():
            directory.mkdir(parents=True)

    def select_files(self, input_list:List[str]):
        has_suffix = True if Path(input_list[0]).suffix else False
        for select in input_list:
            for file in os.listdir(self.base_path):
                if ((has_suffix and Path(file).name.endswith(select)) or
                    (not has_suffix and Path(file).stem.endswith(select))
                ):
                    yield self.base_path.joinpath(file)

    def copy(self, dest:Path, input_list:List[str]):
        """ Copy input_list images from base to dest """
        self.prepare_dir(dest)
        prefix = "[DRY_RUN] Would copy" if self.dry_run else "Copying"
        for selected in self.select_files(input_list):
            print(f"{prefix} {selected} to {dest}...")
            if not self.dry_run:
                shutil.copy(selected, dest)
    
    def move(self, dest:Path, input_list:List[str]):
        """ Move input_list images from base to dest """
        self.prepare_dir(dest)
        prefix = "[DRY_RUN] Would move" if self.dry_run else "Moving"
        for selected in self.select_files(input_list):
            print(f"{prefix} {selected} to {dest}...")
            if not self.dry_run:
                shutil.move(selected.resolve().as_posix(), dest.resolve().as_posix())

    def compare(self, compare_with: Path):
        compare_with = Path(compare_with) if isinstance(compare_with, str) else compare_with
        """ Compare folder with base and remove images from this to look like as base"""
        stayable = set([p.stem for p in self.base_path.iterdir()])
        compared = set([p.stem for p in compare_with.iterdir()])
        to_be_remove = compared.difference(stayable)
        suffix = next(compare_with.iterdir()).suffix()
        for item in to_be_remove:
            print(f"Will remove {item}")
        # raise NotImplemented
                
    def get_files(self, folder: Union[str, Path]) -> set:
        _folder = Path(folder) if isinstance(folder, str) else folder
        
        filenames = {Path(file).stem for file in os.listdir(_folder)}
        return filenames


def parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-b", "--base-path", required=True, help="The base path of the images")
    arg_parser.add_argument("-i", "--inputs", nargs="+", help="The name of images or numbering of images")
    arg_parser.add_argument("-d", "--delete", help="Delete from [base-path] folder", action="store_true")
    arg_parser.add_argument("-m", "--move", help="Use this if you want to move the [inputs] better images and move to [output] folder", 
                            action="store_true")
    arg_parser.add_argument("-c", "--copy", help="Use this if you want to copy the [inputs] better images and move to [output]",
                            action="store_true")
    arg_parser.add_argument("-o", "--output", dest="output", help="Destination folder where to move the selected images")
    arg_parser.add_argument("--dry-run", dest="dry_run", action="store_true")
    arg_parser.add_argument("-C", "--compare", dest="compare", action="store_true", help="Destination folder where to move the selected images")

    # arg_parser.add_help()
    return arg_parser

def main():
    arg_parser = parser()
    args = arg_parser.parse_args()
    # return
    # get jpegs
    print(args.dry_run)
    # return
    base_path = Path(args.base_path)
    image_sorter = ImageSorter(base_path, args.dry_run)
    print(f"base path is: {base_path}")
    if args.inputs:
        input_images = args.inputs
        image_sorter.input_list = input_images
        destination = ""
        if (args.copy or args.move) and "output" not in args:
            print("[output] must be given for using copy and move")
        else:
            # TODO: create destination folder
            destination = args.output
            pass 
        if args.copy:
            image_sorter.copy(dest=destination, input_list=input_images)
        elif args.move:
            image_sorter.move(dest=destination, input_list=input_images)
    elif args.compare:
        destination = args.output
        image_sorter.compare(destination)







if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n')
        exit(0)
