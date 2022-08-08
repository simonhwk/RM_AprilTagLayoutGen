import argparse
import math
from pdf2image import convert_from_path
import apriltag
import cv2
import numpy as np

# parse commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument("target", 
                    help="a pdf or image file")
parser.add_argument("--verbose", 
                    action="store_true",
                    help="turn on --verbose to display the annotated image after detection")
args = parser.parse_args()
filename = args.target

# open pdf or image file
try:
    file_format = filename.split('.')[1]
    if file_format == 'pdf':
        images = [np.array(page) for page in convert_from_path(filename, 500)]
    else:
        image = cv2.imread(filename)
        images = [image]
except:
    print("An exception occurred when openning the file. Check if filename is correct") 


# create cv2 window
if args.verbose:
    cv2.namedWindow('Image with detected tags', cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Image with detected tags", 1000, 1200)
scale = images[0].shape[0] / 5500
params = {
    'circle_size': math.ceil(20 * scale),
    'font_scale': round(2 * scale, 1),
    'font_thickness': math.ceil(5* scale),
    'box_thickness': math.ceil(15 * scale),
    'dx': math.ceil(50 * scale),
    'dy': math.ceil(-250 * scale)
}

# detect and draw tags
print(f'total images: {len(images)}')
print('detecting ...')
for i in range(len(images)):
    print(f'----------------tags detected in image {i + 1}--------------')
    #img = cv2.flip(images[i], -1)
    img = images[i]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detector = apriltag.Detector()
    result = detector.detect(gray)
    ids = []
    for r in result:
        (ptA, ptB, ptC, ptD) = r.corners
        #print(r.tag_id)
        if not r.tag_id in ids:
            ids.append(r.tag_id)
        if args.verbose:
            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))
            ptA = (int(ptA[0]), int(ptA[1]))
            # draw the bounding box of the AprilTag detection
            cv2.line(img, ptA, ptB, (0, 255, 0), params['box_thickness'])
            cv2.line(img, ptB, ptC, (0, 255, 0), params['box_thickness'])
            cv2.line(img, ptC, ptD, (0, 255, 0), params['box_thickness'])
            cv2.line(img, ptD, ptA, (0, 255, 0), params['box_thickness'])
            # draw the center (x, y)-coordinates of the AprilTag
            (cX, cY) = (int(r.center[0]), int(r.center[1]))
            cv2.circle(img, (cX, cY), params['circle_size'], (0, 0, 255), -1)
            
            #draw corner points
            cv2.circle(img, (ptA[0], ptA[1]), params['circle_size'], (0, 0, 255), -1)
            cv2.circle(img, (ptB[0], ptB[1]), params['circle_size'], (5, 185, 250), -1)
            cv2.circle(img, (ptC[0], ptC[1]), params['circle_size'], (86, 245, 237), -1)
            cv2.circle(img, (ptD[0], ptD[1]), params['circle_size'], (25, 144, 3), -1)
            
            cv2.putText(img, str(r.tag_id), (cX+params['dx'], cY+params['dy']),cv2.FONT_HERSHEY_SIMPLEX, params['font_scale'], (255, 0, 0), params['font_thickness'])
            # draw the tag family on the image
            tagFamily = r.tag_family.decode("utf-8")
            # cv2.putText(img, tagFamily, (ptA[0], ptA[1] - 15),
            #     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (105, 240, 60), 2)
            #print("[INFO] tag family: {}".format(tagFamily))
    print(ids)
    if args.verbose:
        cv2.imshow('Image with detected tags', img)
        cv2.waitKey()