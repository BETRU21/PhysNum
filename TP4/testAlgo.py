from util import readAngles, readSinogram
import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import iradon
import matplotlib.image as mpimg

# x, y, sinogram = readSinogram("data/sinogram-patient.txt")
# y, angles = readAngles("data/angles.txt")

# sinogramExample = np.swapaxes(sinogram, 0,1)
# sinogramExample = np.flip(sinogramExample,0)
# image_reconstruite = iradon(sinogramExample, theta=angles*180/np.pi, circle=True)

# fig, ax = plt.subplots(nrows=1, ncols=2)
# ax[0].imshow(sinogram, cmap="gray")
# ax[1].imshow(image_reconstruite, cmap="gray")
# plt.show()

img = mpimg.imread('phantom-thorax-096-smooth.png')
print(img.shape)
