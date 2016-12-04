from PIL import Image, ImageFilter
import math
import numpy as np
from scipy import ndimage, misc
import sys
import csv
import subprocess
from os import listdir, path

def getAngle(filename):
    image = Image.open(filename)

    imageArray = np.array(image.getdata()).reshape((image.size[1], image.size[0]))

    filter_blurred_f = ndimage.gaussian_filter(imageArray, 1)
    alpha = 30
    imageArray = imageArray + alpha * (imageArray - filter_blurred_f)

    maxVal = np.max(imageArray)*1.0
    imageArray = np.round(imageArray/maxVal*255)
    newImage = Image.fromarray(np.uint8(imageArray))
    newImage.save("unblurred.jpg")

    horizontalKernel = np.array([[0,0,0],[-1,0,1],[0,0,0]])
    verticalKernel = np.array([[0, -1, 0], [0,0,0], [0,1,0]])
    size = (3,3)

    horizontal = ndimage.convolve(imageArray, horizontalKernel)
    # horizontal = image.filter(ImageFilter.Kernel(size, horizontalKernel))
    # horizontal.save('burrito_cat_horizontal.jpg')

    vertical = ndimage.convolve(imageArray, verticalKernel)
    # vertical.save('burrito_cat_vertical.jpg')

    horData = horizontal.flatten()
    verData = vertical.flatten()

    newPixels = []

    for i in range(len(horData)):
        angle = math.atan2(verData[i],horData[i]) + math.pi
        newPixels.append(0.5*angle/math.pi*255)
    pixelArray = np.uint8(newPixels).reshape((image.size[1], image.size[0]))
    return pixelArray

empty = getAngle("data/Originals/D10415/1.tiff")
some = getAngle("data/Originals/D10415/9.tiff")
newImage = Image.fromarray(some - empty)
newImage.save("angle.jpg")
