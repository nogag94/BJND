#-*- coding: utf-8 -*-
'''
 Reference: Binocular Just-Noticeable-Difference Model for Stereoscopic Images 
            # Autors: Yin Zhao, Zhenzhong Chen, Member, IEEE, Ce Zhu, Yap-Peng Tan, Senior Member, IEEE, and Lu Yu
 This algorithm calculates the maximum background luminance changes that can be modified in an image before the HVS perceives them
 Keywords:
        - Edges
        - Background Luminance
        - Texture
'''

import random
import numpy as np
import math
import cv2

HSOBEL_WEIGHTS = np.array([[ 1, -2, 0, 2, 1],
                           [ -2, -3, 0, 3, 2],
                           [ -3, -5, 0, 5, 3],
                           [ -2, -3, 0, 3, 2],
                           [-1,-2,-0, 2, 1]])
VSOBEL_WEIGHTS = HSOBEL_WEIGHTS.T

def A_limit(background):
    res = 0
    if background >= 0 and background < 48:
        res = 0.0027 * ((background**2) - (96 * background)) + 8
    elif background >= 48 and background <= 255:
        res = 0.0001 * ((background**2) - (32 * background)) + 1.7
    return res

def eh (image,windowsize_y = 5, windowsize_x = 5):
    axis_y = image.shape[0]
    axis_x = image.shape[1]
    edge = np.zeros((image.shape[0], image.shape[1]))
    for y in range(0,axis_y - windowsize_y):
        for x in range(0,axis_x - windowsize_x):
            window = image[y:y+windowsize_y, x:x+windowsize_x]
            Gx = sum_matrix(HSOBEL_WEIGHTS * window)/25
            Gy = sum_matrix(VSOBEL_WEIGHTS * window)/25
            edge [y,x] = math.sqrt((math.fabs(Gx))**2 + (math.fabs(Gy))**2)
    np.savetxt("edges.txt", edge, fmt='%10.2f')
    return edge
    
def AC_limit(background,edge):
    
    ac_limit = A_limit(background) + ( K(background) * edge) 
    return ac_limit

def K(background):
    if background >=0 and background <= 255:
        k = (-10 ** -6) * ((0.7 * (background ** 2)) + (32 * background)) + 0.07    
    else:
        print 'Valor fuera del rango'
        k = None
    return k

def bjnd_zhao(image, edges):
    coords = {}
    axis_y = image.shape[0]
    axis_x = image.shape[1]
    bjnd_final = np.zeros((image.shape[0], image.shape[1]), np.uint8)
    bjnd_matrix = np.zeros((axis_y,axis_x))
    for y in range(0,axis_y):
        for x in range(0, axis_x):
            bg = image[y,x]
            eh = edges[y,x]
            val = AC_limit(bg, eh)
            bjnd_final[y, x] = val
    return bjnd_final

def background_avg(image):
    background = np.zeros((image.shape[0], image.shape[1],1), np.uint8)
    axis_y = image.shape[0]
    axis_x = image.shape[1]
    for y in range(2,axis_y-1):
        for x in range(2, axis_x-1):
            window = image[y-2:y+3 , x-2:x+3]
            window[2,2] = 0
            background[y,x] = sum_matrix(window) / 24
    return background
            
def sum_matrix(matrix):
    y_axis = matrix.shape[0]
    x_axis = matrix.shape[1]
    sum = 0
    for y in range(0,y_axis):
        for x in range(0,x_axis):
            sum += matrix[y,x]
    return sum

def max(num1, num2):
    if num1 > num2:
        max = num1
    else:
        max = num2
    return max        

def umbral_canny(image):
    edges = cv2.Canny(image,100,150)
    edges[edges==255] = 1
    axis_y = edges.shape[0]
    axis_x = edges.shape[1]
    windowsize_y = 5
    windowsize_x = 5
    k = 5
    rho = np.ones((edges.shape[0], edges.shape[1]))
    c = 0
    for y in range(0,axis_y - windowsize_y):
        for x in range(0,axis_x - windowsize_x):
            window = edges[y:y+windowsize_y, x:x+windowsize_x]
            sum_win = sum_matrix(window)/float(k*k)
            rho[y:y+windowsize_y, x:x+windowsize_x] = sum_win

    pixel_type = np.zeros((edges.shape[0], edges.shape[1]))
    texture = np.zeros((edges.shape[0], edges.shape[1]))

    # Umbralización para la imagen
    for y in range(0,axis_y):
        for x in range(0, axis_x):
            if rho[y,x] < 0.1:
                texture[y,x] = 0
                pixel_type[y,x] = 0
            elif rho[y,x] >= 0.1 and rho[y,x] <= 0.2 :
                texture[y,x] = 0
                pixel_type[y,x] = 255            
            elif rho[y,x] > 0.2:
                texture[y,x] = float((rho[y,x]- 0.2) / 0.8)
                pixel_type[y,x] = 128
    return rho, pixel_type, texture


def bjnd_texture(image,texture):
    coords = {}
    axis_y = image.shape[0]
    axis_x = image.shape[1]
    bjnd_final = np.zeros((image.shape[0], image.shape[1]), np.uint8)
    for y in range(0,axis_y):
        for x in range(0, axis_x):
            bg = image[y,x]
            tex = texture[y,x]
            bjnd_final[y, x] = A_limit(bg) + (tex*8)
    return bjnd_final 

def numbits(bjnd_values):
    total_bits = 0
    axis_y = bjnd_values.shape[0]
    axis_x = bjnd_values.shape[1]
    for y in range(0,axis_y):
        for x in range(0, axis_x):
            val = bjnd_values[y,x]
            total_bits = total_bits + int( math.ceil(math.log(val+1)/math.log(2)))
    return total_bits