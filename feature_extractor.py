from PIL import Image, ImageFilter
import math
import numpy as np
from scipy import ndimage
import sys
import csv
import subprocess
from os import listdir, path
from fft_extractor import fftExtractor

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
    smallX = 1000
    smallY = 1000
    shape = None
    for filename in dirFiles:
        if not filename.endswith('tiff'):
            continue
        image = np.array(Image.open(directory_name + filename))
        if image.shape[1] < 30 or image.shape[0] < 30:
            print filename, "IS TOO SMALL"
            continue
        if image.shape[1] < smallX and image.shape[1] > 30:
            smallX = image.shape[1]
        if image.shape[0] < smallY and image.shape[0] > 30:
            smallY = image.shape[1]
    return (smallY, smallX)


def ExtractAllFeatures(directory_name, dirFiles, extractFn=RawPixelExtractor):
    resultMap = {}
    shape = GetShapeDimensions(directory_name, dirFiles)
    print shape
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
            if count > 1:
                count = 2 # since we only care about 0, 1, or more than 1
            if filenum not in featureMap:
                continue # some images are missing even though the csv contains info
            outList = list(featureMap[filenum])
            outList.append(count)
            # print len(outList)
            if len(outList) < 676:
                print "FOUND AN ISSUE WITH FILE", filenum
                continue # image size is too small
            wr.writerow(outList)

def RunExtraction(directory_name):
    dirFiles = listdir(directory_name)
    csvs = [f for f in dirFiles if f.endswith('csv')]
    countFilename = directory_name + csvs[0]
    foldername = directory_name.split("/")
    foldername = foldername[-2]
    fileCountMap = CreateCountMap(countFilename)
    featureMap = ExtractAllFeatures(directory_name, dirFiles, fftExtractor)
    print "Done processing files"
    WriteOutputFile(foldername, fileCountMap, featureMap)
    return foldername + ".csv"
