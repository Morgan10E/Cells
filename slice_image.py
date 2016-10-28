from PIL import Image
import numpy as np
import sys

if len(sys.argv) < 3:
    print "Please specify the input image and output name. ie. python slice_image.py Images/Image_0006_0000.jpg Images/Chunks/pretty_chunks"
    sys.exit()
image_filename = sys.argv[1]
destination_filename = sys.argv[2]
im = Image.open(image_filename)
# im = im.convert('1')

pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

numSlices = 6
sWidth = width/numSlices
sHeight = height/numSlices

grid = np.array(pixels)
slices = []
for i in range(0,numSlices):
    for j in range(0, numSlices):
        slices.append(grid[(i * sWidth) : ((i+1) * sWidth - 1), (j * sHeight) : ((j+1) * sHeight - 1)])


for i in range(0, len(slices)):
    chunk = slices[i]
    print chunk.shape
    chunk = np.uint8(chunk)
    newImage = Image.fromarray(chunk)
    newImage.save(destination_filename + str(i) + '.png')
