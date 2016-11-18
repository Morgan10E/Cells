from PIL import Image, ImageFilter
import math
import numpy as np
from scipy import ndimage
import sys
from os import listdir, path

if len(sys.argv) < 2:
    print "Please specify the directory and number of files to put into the csv ie python csv_writer.py data_directory 100"
    sys.exit()
directory_name = sys.argv[1]

dirFiles = listdir(directory_name)
for filename in dirFiles:
    if not filename.endswith('tiff'):
        continue
    image = Image.open(directory_name + filename)

    imageArray = np.array(image.getdata()).reshape((image.size[1], image.size[0]))
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

    # newPixels = []

    # for i in range(len(horData)):
    #     angle = math.atan2(verData[i],horData[i]) + math.pi
    #     newPixels.append(0.5*angle/math.pi*255)
    # pixelArray = np.uint8(newPixels).reshape((vertical.size[1], vertical.size[0]))
    # newImage = Image.fromarray(pixelArray)
    # newImage.save("burrito_cat_angle.jpg")


    numBins = 16
    binSize = 2*math.pi/numBins

    # angleArray = numBins*[0]
    # magnitudeArray = numBins*[0]
    histogram = numBins*[0]
    counts = numBins*[0]
    #
    # smallest = float('inf')
    # biggest = float('-inf')

    for i in range(len(horData)):
        angle = math.atan2(verData[i], horData[i]) + math.pi
        # if horData[i] > biggest:
        #     biggest = horData[i]
        # if horData[i] < smallest:
        #     smallest = horData[i]
        # angleArray.append(angle)
        magnitude = math.hypot(verData[i], horData[i])
        # magnitudeArray.append(magnitude)
        binIdx = int(angle/binSize)%numBins
        counts[binIdx] += 1
        remainder = angle%binSize - binSize/2
        nextBinIdx = (binIdx - 1)%numBins
        if remainder > 0:
            nextBinIdx = (binIdx + 1)%numBins
        histogram[binIdx] += (binSize - abs(remainder))/binSize*magnitude
        histogram[nextBinIdx] += abs(remainder)/binSize*magnitude
    print histogram
    # print counts
    # print '.'

# print biggest
# print smallest
