#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TP reconstruction TDM (CT)
# Prof: Philippe Després
# programme: Dmitri Matenine (dmitri.matenine.1@ulaval.ca)


# libs
import numpy as np
import time

# local files
import geo as geo
import util as util
import CTfilter as CTfilter

## créer l'ensemble de données d'entrée à partir des fichiers
def readInput():
    # lire les angles
    [nbprj, angles] = util.readAngles(geo.dataDir+geo.anglesFile)

    print("nbprj:",nbprj)
    print("angles min and max (rad):")
    print("["+str(np.min(angles))+", "+str(np.max(angles))+"]")

    # lire le sinogramme
    [nbprj2, nbpix2, sinogram] = util.readSinogram(geo.dataDir+geo.sinogramFile)

    if nbprj != nbprj2:
        print("angles file and sinogram file conflict, aborting!")
        exit(0)

    if geo.nbpix != nbpix2:
        print("geo description and sinogram file conflict, aborting!")
        exit(0)

    return [nbprj, angles, sinogram]


## reconstruire une image TDM en mode rétroprojection
def laminogram_with_for_loop():
    [nbprj, angles, sinogram] = readInput()
    image = np.zeros((geo.nbvox, geo.nbvox))
    center = geo.nbvox // 2

    # "Étaler" les projections sur l'image
    # Ceci sera fait de façon "voxel-driven"
    # Pour chaque voxel, trouver la contribution du signal reçu
    for j in range(geo.nbvox):  # Colonnes de l'image
        print("working on image column: " + str(j + 1) + "/" + str(geo.nbvox))
        for i in range(geo.nbvox):  # Lignes de l'image
            for a in range(len(angles)):
                angle = angles[a]
                det_pos = (j - center) * np.cos(angle) + (i - center) * np.sin(angle)
                det_index = int(np.round(det_pos + len(sinogram[0]) / 2))
                if det_index >= 0 and det_index < len(sinogram[0]):
                    image[i, j] += sinogram[a, det_index]
    util.saveImage(image, "lam")

def laminogram():
    nbprj, angles, sinogram = readInput()
    image = np.zeros((geo.nbvox, geo.nbvox))

    center = geo.nbvox // 2

    x_coords, y_coords = np.meshgrid(np.arange(geo.nbvox), np.arange(geo.nbvox))
    x_coords_centered = x_coords - center
    y_coords_centered = y_coords - center

    det_pos = x_coords_centered[..., None] * np.cos(angles) + y_coords_centered[..., None] * np.sin(angles)
    det_indices = np.round(det_pos + len(sinogram[0]) / 2).astype(int)
    det_indices = np.clip(det_indices, 0, len(sinogram[0]) - 1)

    for a in range(len(angles)):
        image += sinogram[a, det_indices[:,:,a]]

    image = np.flip(image,1)
    util.saveImage(image, "lam")


## reconstruire une image TDM en mode retroprojection filtrée
def backproject():
    
    [nbprj, angles, sinogram] = readInput()
    
    # initialiser une image reconstruite
    image = np.zeros((geo.nbvox, geo.nbvox))
    
    ### option filtrer ###
    CTfilter.filterSinogram(sinogram)
    ######
    
    # "etaler" les projections sur l'image
    # ceci sera fait de façon "voxel-driven"
    # pour chaque voxel, trouver la contribution du signal reçu
    for j in range(geo.nbvox): # colonnes de l'image
        print("working on image column: "+str(j+1)+"/"+str(geo.nbvox))
        for i in range(geo.nbvox): # lignes de l'image
            for a in range(len(angles)):
                pass
                #votre code ici
               #pas mal la même chose que prédédemment
                #mais avec un sinogramme qui aura été préalablement filtré

    util.saveImage(image, "fbp")


## reconstruire une image TDM en mode retroprojection
def reconFourierSlice():
    
    [nbprj, angles, sinogram] = readInput()

    # initialiser une image reconstruite, complexe
    # pour qu'elle puisse contenir sa version FFT d'abord
    IMAGE = np.zeros((geo.nbvox, geo.nbvox), 'complex')
    
    # conteneur pour la FFT du sinogramme
    SINOGRAM = np.zeros(sinogram.shape, 'complex')

    #image reconstruite
    image = np.zeros((geo.nbvox, geo.nbvox))
    #votre code ici
   #ici le défi est de remplir l'IMAGE avec des TF des projections (1D)
   #au bon angle.
   #La grille de recon est cartésienne mais le remplissage est cylindrique,
   #ce qui fait qu'il y aura un bon échantillonnage de IMAGE
   #au centre et moins bon en périphérie. Un TF inverse de IMAGE vous
   #donnera l'image recherchée.

   
    
    util.saveImage(image, "fft")


## main ##
start_time = time.time()
laminogram()
#backproject()
#reconFourierSlice()
print("--- %s seconds ---" % (time.time() - start_time))

