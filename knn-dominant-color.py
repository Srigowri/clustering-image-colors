# -*- coding: utf-8 -*-
"""The code is used to find the most dominant color in terms of RGB
using K means clustering algorithm

Example:
    Given an image as input the program, it outputs the RGB components of
    of the most dominant color found in the image.
Attributes:
    Point, a named tuple
    CLuster, a named tuple
Todo:
    Run the code on the test images 
"""

import matplotlib.colors as colors
import random
import urllib.request

import tkinter as tk
from tkinter import filedialog


from collections import namedtuple
from math import sqrt
from PIL import Image


min_diff = 1
Point = namedtuple('Point', ('coords', 'num_of_coords', 'count'))
Cluster = namedtuple('Cluster', ('points', 'center', 'num_of_coords'))

"""namedtuple is a function implemented in the collection module.
It is used to create tuples with named fields

Point(named tuple): The first argument is the type name and 
the field names are coords,num_of_coords (3 since we want only RGB) and counts
The tuples's values can be accessed using the field names

Cluster(named tuple):The first argument is the type name and 
the field names are points, center and num_of_coords

For more info on namedtuple, use the following link:
https://docs.python.org/3/library/collections.html#collections.namedtuple 

"""

root = tk.Tk()
root.withdraw()

def main():
    """This function takes the image as an input from the file dialog
    
    """
    imagefile = filedialog.askopenfilename()
    x = get_dominant_colors(imagefile)
    for value in x:
        print(value)
        # newstring = value.replace("#","")
        # print("http://www.colorhexa.com/"+newstring+".png")
        # urllib.request.urlretrieve("http://www.colorhexa.com/"+newstring+".png","C:/Users/P A Vijaya/Desktop/Programs/color.png")
        rgb=colors.hex2color(value)
        #note !!!! receive as list
        return([int(255*value) for value in rgb])
    
def get_dominant_colors(filename, k=3):
    """The function is responsible for reading the input image, reducing the image size
     while keeping the same aspect ratio and perform k means clustering on the pixel values with 3 clusters
    
    Args:
        param1 (string): Filename of the image
        param2 (int,optional): Number of clusters
    
    Returns:
        Values of RGB in hexadecimal
    
    Todo:
        Find a better method to resize image
    """
    
    img = Image.open(filename)
    #reduce image size
    img.thumbnail((200, 200))
    #w, h = img.size
    points = get_points(img)
    clusters = kmeans(points, k,min_diff)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def get_points(img):
    """This module returns a list of named tuple where each tuple has the 
    color(rgb) and index
    
    getcolors returs a tuple(count,color) or none.
    w*h is maxcolors
    
    Point(coords=(252, 127, 41), num_of_coords=3, count=1)
    """
    points = []
    w, h = img.size
    for index, color in img.getcolors(w * h):
        points.append(Point(color, 3, index))
    return points



def kmeans(points, k, min_diff):
    """This function implements k means algorithm to find centers of 3 clusters.
    
    Args:
        param1(namedtuple): list of points. Each point has 3 fields
        1st field is the rgb values,number of coordinates and an index
        param2(k:int): Number of clusters
        param3(min_diff:int): Terminating condition for the k means
        
    """
    #Randomly select 3 points as the initial centers of 3 clusters
    clusters = [Cluster([p], p, p.num_of_coords) for p in random.sample(points, k)]

    while True:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                #find the closest center to the point p
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.num_of_coords)
            new = Cluster(plists[i], center, old.num_of_coords)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters


def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.num_of_coords)
    ]))


def calculate_center(points, n):
    """This function will find the weighted average of R,G and B components
    for all the points
    Args:
        param1(points:list of tuple)
        param2(n:int): 3 representing R,G and B
    
    """
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.count
        for i in range(n):
            vals[i] += (p.coords[i] * p.count)
    return Point([(v / plen) for v in vals], n, 1)



print(main())
