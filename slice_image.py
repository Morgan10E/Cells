from PIL import Image
import numpy as np

im = Image.open('Images/example1.jpg')
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
    newImage.save('Sliced/chunk' + str(i) + '.png')
