# libs
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from scipy import interpolate
import matplotlib.cm as cm
import time

##### util FILE #####
#####################

def readAngles(filename):

    angles = np.loadtxt(filename)
    nbprj = angles.shape[0]

    # convertir en radians element par element
    angles = (np.pi/180.0)*angles

    return [nbprj, angles]


## lire un sinogramme
def readSinogram(filename):
    
    sino = np.loadtxt(filename)
    nbprj = sino.shape[0]
    nbpix = sino.shape[1]

    return [nbprj, nbpix, sino]

##### geo FILE #####
####################

### paramètres d'acquisition ###

## largeur d'un élément de détecteur (cm)
pixsize = 0.165

## taille du détecteur (nombre d'échantillons)
nbpix = 336

### paramètres de reconstruction ###

## taille de la grille d'image (carrée)
nbvox = 96 # options: 96, 192

## taille du voxel (carré) (cm)
voxsize = 0.4 # option: 0.4, 0.2

## fichiers d'entrée
dataDir = "./data/"
anglesFile = "angles.txt"
# sinogramFile = "sinogram-password.txt"
sinogramFile = "sinogram-patient.txt"

##### CTfilter FILE #####
#########################

def filterSinogram(sino):
    for i in range(sino.shape[0]):
        sino[i] = filterLine(sino[i])
    return sino

## filter une ligne (projection) via FFT
def filterLine(projection):
    fft_signal = np.fft.fftshift(np.fft.fft(projection))  # Transformation de Fourier
    fft_signal_filtered = fft_signal.copy()  # Copie du signal transformé

    length = len(fft_signal_filtered)
    if length%2:
        maxi = np.round(length/2)
        mini = maxi-1
        ramp_filter = np.abs(np.arange(-mini, maxi) / mini)
    else:
        mini = int(length/2)
        maxi = mini+1
        ramp_filter = np.abs(np.arange(-mini, maxi) / mini)
        ramp_filter = np.delete(ramp_filter, mini)

    fft_signal_filtered = fft_signal_filtered*ramp_filter


    return np.fft.ifft(np.fft.ifftshift(fft_signal_filtered)).real

def laminogram(filename):
    # Import
    [nbprj, angles] = readAngles(dataDir+anglesFile)
    [nbprj2, nbpix2, sino] = readSinogram(dataDir+filename)
    image = np.zeros((nbvox, nbvox))

    # Coordonnées
    center = nbvox // 2
    x_coords, y_coords = np.meshgrid(np.arange(nbvox), np.arange(nbvox))
    x_coords_centered = x_coords - center
    y_coords_centered = y_coords - center

    # Reconstruction
    det_pos = x_coords_centered[..., None] * np.cos(angles)*voxsize/pixsize + y_coords_centered[..., None] * np.sin(angles)*voxsize/pixsize
    det_indices = np.round(det_pos + len(sino[0]) / 2).astype(int)
    det_indices = np.clip(det_indices, 0, len(sino[0]) - 1)
    for a in range(len(angles)):
        image += sino[a, det_indices[:,:,a]]

    return np.flip(image,1)

sino_patient = laminogram("sinogram-patient.txt")
sino_ref = mpimg.imread('phantom-thorax-096-smooth.png')

# fig, ax = plt.subplots(nrows=1, ncols=2,figsize=(12,12))
# ax[0].axis("off")
# ax[1].axis("off")
# ax[0].set_title("Image de référence")
# ax[1].set_title("Reconstruction par laminogramme")
# ax[0].imshow(sino_ref, cmap="gray")
# ax[1].imshow(sino_patient, cmap="gray")
# plt.show()

[nbprj, angles] = readAngles(dataDir+anglesFile)
[nbprj2, nbpix2, sinogram] = readSinogram(dataDir+"sinogram-patient.txt")

sinogram_filtre = filterSinogram(sinogram.copy())

fig, ax = plt.subplots(nrows=1, ncols=2,figsize=(6,6))
ax[0].axis("off")
ax[1].axis("off")
ax[0].set_title("Sinogramme non filtré")
ax[1].set_title("Sinogramme filtré")
ax[0].imshow(sinogram, cmap="gray")
ax[1].imshow(sinogram_filtre, cmap="gray")
plt.show()