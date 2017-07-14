#-*- coding: utf-8 -*-
'''
 This script modify gray-scale image with BJND values to every test image from Middlebury database.
'''
import cv2
from bjnd_model import *
import numpy as np

def get_image_modified(path, filename):    
    # Set path
    image = path + filename
    # Get color image
    gray_image = cv2.imread(image, 0)

    # BJND - ZHAO
    # Calculate edge height
    # edges = eh(gray_image)

    # BJND - NORIEGA
    # Calculate texture using Canny edge detection
    rho,imagen,texture = umbral_canny(gray_image)

    # Background Luminance average
    image = background_avg(gray_image)

    # Calculate BJND - ZHAO
    # bjnd_vals = bjnd_zhao(image, edges)

    # Calculate BJND - ZHAO
    bjnd_vals = bjnd_texture(image, texture)
    
    # Original image + BJND values
    original =  cv2.imread(path + filename, 0)
    prueba = np.zeros((original.shape[0], original.shape[1]))
    prueba = original + bjnd_vals
    cv2.imwrite(filename, prueba)

if __name__=='__main__':

    '''filenames_left = ['Adirondack0.png','ArtL0.png','Jadeplant0.png','Motorcycle0.png','MotorcycleE0.png','Piano0.png','PianoL0.png',
                 'Pipes0.png','Playroom0.png','Playtable0.png','PlaytableP0.png','Recycle0.png','Shelves0.png','Teddy0.png','Vintage0.png']'''
    
    filenames_right = ['Adirondack1.png','ArtL1.png','Jadeplant1.png','Motorcycle1.png','MotorcycleE1.png','Piano1.png','PianoL1.png',
                 'Pipes1.png','Playroom1.png','Playtable1.png','PlaytableP1.png','Recycle1.png','Shelves1.png','Teddy1.png','Vintage1.png']
    
    path = '.\Yimages\\'

    '''for name in filenames_left:
        get_image_modified(path, name)'''

    for name in filenames_right:
        get_image_modified(path, name)
    