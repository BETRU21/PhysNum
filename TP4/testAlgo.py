from util import readAngles, readSinogram
import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import iradon
import matplotlib.image as mpimg
from scipy import interpolate

def indices_ligne_centrale_angle(array_shape, angle_radian):
    # Trouver les coordonnées du centre du tableau
    center = np.array(array_shape) / 2

    # Calculer les déplacements horizontaux et verticaux pour chaque position le long de la ligne
    dx = np.cos(angle_radian)
    dy = np.sin(angle_radian)

    # Générer les indices le long de la ligne en utilisant du slicing
    x_indices = np.arange(array_shape[0])
    y_indices = np.arange(array_shape[1])
    x_centered = x_indices - center[0]
    y_centered = y_indices - center[1]
    x_line = np.round(x_centered + dx * y_centered / dy).astype(int)
    y_line = np.round(y_centered + dy * x_centered / dx).astype(int)

    # Sélectionner les indices valides qui se trouvent à l'intérieur du tableau
    valid_indices = np.logical_and(x_line >= 0, x_line < array_shape[0])
    valid_indices &= np.logical_and(y_line >= 0, y_line < array_shape[1])
    x_line = x_line[valid_indices]
    y_line = y_line[valid_indices]

    # Retourner les indices de la ligne
    return list(zip(x_line, y_line))

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

# sinogramExample = np.swapaxes(sinogram, 0,1)
# sinogramExample = np.flip(sinogramExample,0)
# image_reconstruite = iradon(sinogramExample, theta=angles*180/np.pi, circle=True)

# fig, ax = plt.subplots(nrows=1, ncols=2)
# ax[0].imshow(sinogram, cmap="gray")
# ax[1].imshow(image_reconstruite, cmap="gray")
# plt.show()


def backproject(filename):
    [nbprj, angles] = readAngles(dataDir+anglesFile)
    [nbprj2, nbpix2, sinogram] = readSinogram(dataDir+filename)
    image = np.zeros((nbvox, nbvox))
    
    ### option filtrer ###
    sinogram = filterSinogram(sinogram)
    ######

    center = nbvox // 2

    x_coords, y_coords = np.meshgrid(np.arange(nbvox), np.arange(nbvox))
    x_coords_centered = x_coords - center
    y_coords_centered = y_coords - center

    det_pos = x_coords_centered[..., None] * np.cos(angles)*voxsize/pixsize + y_coords_centered[..., None] * np.sin(angles)*voxsize/pixsize
    det_indices = np.round(det_pos + len(sinogram[0]) / 2).astype(int)
    det_indices = np.clip(det_indices, 0, len(sinogram[0]) - 1)

    for a in range(len(angles)):
        image += sinogram[a, det_indices[:,:,a]]

    image = np.flip(image,1)
    return image

def reconFourierSlice(filename):
	# Import
    [nbprj, angles] = readAngles(dataDir+anglesFile)
    [nbprj2, nbpix2, sinogram] = readSinogram(dataDir+filename)

    # Coordonnées polaire
    xy = np.arange(nbvox//2, -nbvox//2, -1)
    grid_x, grid_y = np.meshgrid(xy, -xy.copy())
    z = np.arange(-nbpix//2, nbpix//2, 1)
    circ_x = np.outer(np.cos(angles), z).ravel()/1.48#(voxsize/pixsize-1)
    circ_y = np.outer(np.sin(angles), z).ravel()/1.48#(voxsize/pixsize-1)

    # Reconstruction
    proj_fft = np.fft.fft(np.fft.ifftshift(sinogram))
    proj_fft = np.fft.fftshift(proj_fft)
    fft2 = interpolate.griddata((circ_x, circ_y),proj_fft.ravel(),(grid_x, grid_y),method="linear",fill_value=0,).reshape((nbvox, nbvox))
    img = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(fft2))).real
    return img





sino_patient = backproject("sinogram-patient.txt")
sino_fourier = reconFourierSlice("sinogram-patient.txt")
sino_ref = mpimg.imread('phantom-thorax-096-smooth.png')

fig, ax = plt.subplots(nrows=2, ncols=3)
ax[0][0].axis("off")
ax[0][1].axis("off")
ax[0][2].axis("off")
ax[0][0].imshow(sino_patient, cmap="gray")
ax[0][1].imshow(sino_fourier, cmap="gray")
ax[0][2].imshow(sino_ref, cmap="gray")

sino_patient = np.fft.fftshift(np.fft.fft(sino_patient))
sino_fourier = np.fft.fftshift(np.fft.fft(sino_fourier))
sino_ref = np.fft.fftshift(np.fft.fft(sino_ref))


ax[1][0].axis("off")
ax[1][1].axis("off")
ax[1][2].axis("off")
ax[1][0].imshow(20*np.log(np.abs(sino_patient)), cmap="gray")
ax[1][1].imshow(20*np.log(np.abs(sino_fourier)), cmap="gray")
ax[1][2].imshow(20*np.log(np.abs(sino_ref)), cmap="gray")
plt.show()
