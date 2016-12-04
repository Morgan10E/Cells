from PIL import Image, ImageFilter
import math
import numpy as np
from scipy import ndimage
import sys
import csv
import subprocess
from os import listdir, path

def CreateCountMap(csvFilename):
    fileCountMap = {}
    penIndex = -1
    countIndex = -1
    with open(csvFilename) as f:
        for line in f:
            vals = line.split(",")
            if penIndex == -1:
                penIndex = vals.index('Pen ID')
                countIndex = vals.index('Cell Count Verified')
                print penIndex, countIndex
                continue
            # print vals
            fileCountMap[vals[penIndex]] = int(vals[countIndex])
    return fileCountMap

def RawPixelExtractor(imageFileName, shape):
    image = np.array(Image.open(imageFileName)) # 16 bit tiff file
    image = image[0:shape[0], 0:shape[1]]
    return np.ravel(image)

def GetShapeDimensions(directory_name, dirFiles):
    smallest = int(1000000000000)
    shape = None
    for filename in dirFiles:
        if not filename.endswith('tiff'):
            continue
        image = np.array(Image.open(directory_name + filename))
        if image.size < smallest:
            smallest = image.size
            shape = image.shape
    return shape


def ExtractAllFeatures(directory_name, dirFiles, extractFn=RawPixelExtractor):
    resultMap = {}
    shape = GetShapeDimensions(directory_name, dirFiles)
    for filename in dirFiles:
        if not filename.endswith('tiff'):
            continue
        filenumber = filename.split(".")
        resultMap[filenumber[0]] = extractFn(directory_name + filename, shape)
    return resultMap

def WriteOutputFile(foldername, fileCountMap, featureMap):
    with open(foldername + ".csv", "w") as myfile:
        wr = csv.writer(myfile)
        for filenum, count in fileCountMap.iteritems():
            if count > 0:
                count = 1 # since we only care about 0, 1, or more than 1
            outList = list(featureMap[filenum])
            outList.append(count)
            wr.writerow(outList)

def RunExtraction(directory_name):
    dirFiles = listdir(directory_name)
    csvs = [f for f in dirFiles if f.endswith('csv')]
    countFilename = directory_name + csvs[0]
    foldername = directory_name.split("/")
    foldername = foldername[-2]
    fileCountMap = CreateCountMap(countFilename)
    featureMap = ExtractAllFeatures(directory_name, dirFiles)
    print "Done processing files"
    WriteOutputFile(foldername, fileCountMap, featureMap)
    return foldername + ".csv"
