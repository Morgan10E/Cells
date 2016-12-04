from PIL import Image, ImageFilter
import math
import numpy as np
from scipy import ndimage
import sys
import csv
import subprocess
from os import listdir, path

if len(sys.argv) < 2:
    print "Please specify the directory and number of files to put into the csv ie python csv_writer.py data_directory 100"
    sys.exit()
directory_name = sys.argv[1]

dirFiles = listdir(directory_name)
csvFilename = directory_name
fileHistMap = {}
fileCountMap = {}
for filename in dirFiles:
    if not filename.endswith('tiff'):
        if filename.endswith('csv'):
            csvFilename += filename
            subprocess.call("cut -d, -f4,6 < " + csvFilename + " > temp.txt", shell=True)
            with open("temp.txt") as f:
                for line in f:
                    if line[0] == 'P':
                        continue
                    vals = line.split(",")
                    fileCountMap[vals[0]] = int(vals[1])
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
    total = 0.0
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
        total += magnitude
        # magnitudeArray.append(magnitude)
        binIdx = int(angle/binSize)%numBins
        counts[binIdx] += 1
        remainder = angle%binSize - binSize/2
        nextBinIdx = (binIdx - 1)%numBins
        if remainder > 0:
            nextBinIdx = (binIdx + 1)%numBins
        histogram[binIdx] += (binSize - abs(remainder))/binSize*magnitude
        histogram[nextBinIdx] += abs(remainder)/binSize*magnitude
    for i in range(numBins):
        histogram[i] /= (total * 1.0)
    filenumber = filename.split(".")
    fileHistMap[filenumber[0]] = histogram
    # print filenumber[0], histogram
    # print counts
    # print '.'
foldername = directory_name.split("/")
foldername = foldername[-2]
avg_hist = [0.0] * numBins
numzeros = 0
for filenum, hist in fileHistMap.iteritems():
    count = fileCountMap[filenum]
    if count == 0:
        numzeros += 1
        for i in range(numBins):
            avg_hist[i] += hist[i]
for i in range(numBins):
    avg_hist[i] /= numzeros

with open(foldername + ".csv", "w") as myfile:
    wr = csv.writer(myfile)
    for filenum, count in fileCountMap.iteritems():
        if count > 2:
            count = 2 # since we only care about 0, 1, or more than 1
        outList = list(fileHistMap[filenum])
        for i in range(numBins):
            outList[i] -= avg_hist[i]
        outList.append(count)
        wr.writerow(outList)
        # print fileHistMap[filenum], ":" + str(count)


# print biggest
# print smallest
