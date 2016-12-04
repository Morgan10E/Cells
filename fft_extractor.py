from PIL import Image
import numpy as np
import math

def convert8Bit(arr):
    maxVal = np.max(arr) * 1.0
    result = np.round(arr / maxVal * 255)
    return result

def fftExtractor(imageFileName, size):
    im = Image.open(imageFileName)
    im_arr = np.array(im)
    im_arr = im_arr[0:size[0], 0:size[1]]
    freq = np.fft.fft2(im_arr)
    freq = np.fft.fftshift(freq)
    freq_abs = np.abs(freq)
    scaled = convert8Bit(freq_abs)

    height = scaled.shape[0]
    width = scaled.shape[1]
    radius = width / 6 * 0.9
    midX = width/2
    midY = height/2
    margin = midX/10
    for x in range(width):
        for y in range(height):
            if not scaled[y, x] == 0:
                dist = math.hypot(midX-x, midY-y)
                if dist > radius:
                    if dist >= margin + radius:
                        freq[y, x] = 0
                    else:
                        freq[y, x] = freq[y,x] * (margin - (dist-radius)) / margin
                #     freq[y,x] = 0

    freq = np.fft.fftshift(freq)
    windowRad = int(radius + margin)
    center_freq = freq[midY - windowRad:midY + windowRad, \
        midX - windowRad:midY + windowRad]
    return np.ravel(center_freq)
