from PIL import Image
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plt

def convert8Bit(arr):
    maxVal = np.max(arr) * 1.0
    result = np.round(arr / maxVal * 255)
    return result

im = Image.open('11.tiff')
im_arr = np.array(im)
freq = np.fft.fft2(im_arr)
freq = np.fft.fftshift(freq)
freq = np.abs(freq)
scaled = convert8Bit(freq)
res = Image.fromarray(scaled)
res.save('freq_shift.tiff')


# fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(14, 6))
# ax[0,0].hist(freq.ravel(), bins=100)
# ax[0,0].set_title('hist(freq)')
# ax[0,1].hist(np.log(freq).ravel(), bins=100)
# ax[0,1].set_title('hist(log(freq))')
# ax[1,0].imshow(np.log(freq), interpolation="none")
# ax[1,0].set_title('log(freq)')
# ax[1,1].imshow(im, interpolation="none")
# plt.show()

# im10 = Image.open('10.png')
# im11 = Image.open('11.png')
# im10_arr = np.array(im10)
# im11_arr = np.array(im11)
#
# new_im_arr = im11_arr - im10_arr
# new_im = Image.fromarray(new_im_arr)
# new_im.save('subtracted.png')
