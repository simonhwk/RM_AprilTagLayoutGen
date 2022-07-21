# RM_AprilTagLayoutGen
python script to generate PDF file with layout for April Tags

# April Tag Strip Generator for the Robot Metabolism Project

[Robert Kasumi]
<br>
Columbia University
<br>

## Overview
This repo contains the script that generates PDF files of April Tag strips to be attached to the Robot Metabolism links.

## Content

- [Installation](#installation)
- [Running the Script]

## Installation

The repository (April Tag Generation script and folder containing images of April Tags) is downloaded using the following command:

```
git clone https://github.com/GitWyd/RM_AprilTagLayoutGen.git
```

Make sure the reportlab tool is also downloaded using:
```
pip install reportlab==3.2.0
```

## Running the Script

First, go into the script and configure your scaling factors. Set tagScale to a negative integer if you wish to size each tag independently.
Then, run the following:

./maketags.sh <list of link numbers>

Alternatively, the script can be run using:

python atagmain.py -i <input file> -l <list of link numbers>

The flag -i is followed by the name of the input file to be read.  
The input file used to generate tags should always be tags36h11_big, as the scaling factors used in atagmain.py were based on the image dimensions in tags36h11_big. 
The flag -l is a list of links that April Tag strips will be generated for. For example, the command line statement 

python atagmain.py -i tags36h11_big_cropped_flipped -l 0 1

Will produce four strips total, the first two for link zero, and the last two for link one.

## Detect Apriltags from images or pdf files
The script `detect_apriltags.py` can be used to detect the apriltags in an image or a multi-page pdf file. `--verbose` draws bounding boxes and ids of detected tags on the images.

**Additional packages required**
`apriltag`, `opencv-python`, `numpy`, `pdf2image`

**Usage**
```
python detect_apriltags.py <FILENAME> --verbose
```
