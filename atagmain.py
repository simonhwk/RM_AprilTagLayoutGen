# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 22:19:31 2021

@author: rkasumi87
@RevisedBy: GitWyd, quinnbooth
"""
import sys
import os
import argparse
import cv2
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib.units import cm
import matplotlib.pyplot as plt

def main(argv):
    #Opens AprilTag File
    linklist = []
    parser = argparse.ArgumentParser(description="Usage: python atagmain.py -i <input file> -l <list of links>")
    parser.add_argument("-i", "--tag_folder", dest='tagfolder', 
                        help='File name containing AprilTag images', required = True)
    
    parser.add_argument("-l", "--list", nargs="+", dest ='linklist', type=int,
                        help='List of links to generate AprilTags for. Ex: 1 5 3', required = True)
    
    args = parser.parse_args()
    tagfolder = args.tagfolder
    image_list = os.listdir(tagfolder)
    linklist = args.linklist
    
    #print(image_list[:20])
    
    canvas = Canvas('tags.pdf', pagesize = LETTER, bottomup=0)
    #canvas.scale(1, -1)
    im_list0 = []
    num_list0 = []
    tag_data0 = []
    
    im_list1 = []
    num_list1 = []
    tag_data1 = []
    
    xoffset = 20
    yoffset = 200
    
    colW = 55
    rowH = 55
    
    ######## CHANGE THIS TO ALTER TAG SCALE ########
    #tagScale = 1.8
    tagScale = -1 # Universal (uniform) scaling. Set it to any negative integer to size each tag independently below.
    
    firstStripScales = [1.8, 1.75, 1.75, 1.75, 1.75, 1.75]
    secondStripScales = [1.75, 1.75, 1.75, 1.8, 1.75, 1.75]
    
    ################################################
    
    # Check if user wants uniform or independent scale factors
    if (tagScale >= 0):
        firstStripScales = []
        secondStripScales = []
        for i in range(6):
            firstStripScales.append(tagScale)
            secondStripScales.append(tagScale)
    
    # Generate output PDF
    tag_counter = 0
    print(linklist)
    for i in linklist:
        #Clear im_list0, num_list0, and tag_data0
        im_list0.clear()
        num_list0.clear()
        tag_data0.clear()
        
        #Clear im_list1, num_list1, tag_data1
        im_list1.clear()
        num_list1.clear()
        tag_data1.clear()
        for a in range(12 * i, 12 * i + 6):
            print('a: ', a)
            #Create list of images and numbers for first strip
            im0_num = str(a).rjust(5, '0')
            im0_fname = f'tag36_11_{im0_num}_big.png'
            print(im0_fname)
            print(os.path.join(tagfolder, im0_fname))
            im0 = Image(os.path.join(tagfolder, im0_fname))
            #im = Imagee.open(os.path.join(tagfolder, im0_fname))
            #im.show()
            im0.drawHeight = firstStripScales[a % 12] * cm
            im0.drawWidth = firstStripScales[a % 12] * cm
            im_list0.append(im0)
            
            num_list0.append(str(a))
            
            im1_num = str(a+6).rjust(5, '0')
            #Create list of images and numbers for second strip
            im1_fname = f'tag36_11_{im1_num}_big.png'
            im1 = Image(os.path.join(tagfolder, im1_fname))
            print(im1_fname)
            print(os.path.join(tagfolder, im1_fname))
            im1.drawHeight = secondStripScales[a % 12] * cm
            im1.drawWidth = secondStripScales[a % 12] * cm
            im_list1.append(im1)
            
            num_list1.append(str(a + 6))
    
        #Append images and numbers of first strip
        tag_data0.append(im_list0)
        tag_data0.append(num_list0)
        
        #Append images and numbers of second strip
        tag_data1.append(im_list1)
        tag_data1.append(num_list1)
        
        #Format strip 1
        table0 = Table(tag_data0, colWidths = colW, rowHeights = rowH)
        table0.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),                      #Horizontal center aligns all entities
            ('VALIGN', (0, 0), (-1, 0), 'CENTER'),                      #Vertical center aligns AprilTags
            ('BOTTOMPADDING', (0, 1), (-1, 1), 40),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
            ]))
        table0.wrapOn(canvas, 0, 0)
        table0.drawOn(canvas, xoffset, 230 * tag_counter + 30)
        
        #Format strip 2
        table1 = Table(tag_data1, colWidths = colW, rowHeights = rowH)
        table1.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'CENTER'), 
            ('BOTTOMPADDING', (0, 1), (-1, -1), 40), 
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.white),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
            ]))
        table1.wrapOn(canvas, 0, 0)
        table1.drawOn(canvas, xoffset, 230 * tag_counter + 100 + 30 + 15)
        
        canvas.rect(350, 230 * tag_counter + 30, colW, 2 * rowH)
        canvas.rect(350, 230 * tag_counter + 100 + 30 + 15, colW, 2 * rowH)
        tag_counter += 1
        if tag_counter and tag_counter%3 == 0:  
            canvas.showPage()
            tag_counter = 0
    canvas.save()
    print("Successfully generated tags!")
     
if __name__ == "__main__":
    main(sys.argv)

