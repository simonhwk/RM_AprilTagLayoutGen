#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 17:17:01 2022

@author: quinnbooth

last modified: Aug 7, 2022 by Qi-Zha0
"""

# Run using:
# python flipcroptags.py -s tag36h11_big -d tag36h11_big_cropped_flipped

import sys
import os
import argparse
from PIL import Image

def main(argv):
    
    # Grab args from user for source/destination directories
    parser = argparse.ArgumentParser(description="Usage: python croptags.py -s <source directory> -d <destination directory>")
    parser.add_argument("-s", "--source_directory", dest='source_directory', 
                        help='Directory containing uncropped April Tags', required = True)
    parser.add_argument("-d", "--destination_directory", dest='destination_directory', 
                        help='Directory to save cropped April Tags', required = True)
    args = parser.parse_args()
    sourceDir = os.listdir(args.source_directory)
    destDir = os.listdir(args.destination_directory)
    
    # Empty destination directory
    for tag in destDir:
        os.remove(os.path.join(args.destination_directory, tag))
    
    # Crop & flip images in source directory and save into destination directory
    for tag in sourceDir:
        currentTag = os.path.join(args.source_directory, tag)
        if not os.path.isfile(currentTag):
            print("Error: found non-file instance in " + args.source_directory)
            break
        pilTag = Image.open(currentTag)
        width, height = pilTag.size
        croppedTag = pilTag.crop((0.1 * width, 0.1 * height, 0.9 * width, 0.9 * height))
        # Report lab flips the image upside down when inserting it to pdf, flip it back:
        flippedCroppedTag = croppedTag.transpose(Image.FLIP_TOP_BOTTOM)
        # Align tag corners
        tag_num = int(tag.split('_')[-2])
        if (tag_num % 12 < 6): #srv0 end
            flippedCroppedRotatedTag = flippedCroppedTag.rotate(90)
        else: #srv1 end
            flippedCroppedRotatedTag = flippedCroppedTag.rotate(-90)
        tagDest = os.path.join(args.destination_directory, tag)
        flippedCroppedRotatedTag.save(tagDest)
        
if __name__ == "__main__":
    main(sys.argv)
