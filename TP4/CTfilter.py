#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TP reconstruction TDM (CT)
# Prof: Philippe Després
# programme: Dmitri Matenine (dmitri.matenine.1@ulaval.ca)


# libs
import numpy as np

## filtrer le sinogramme
## ligne par ligne
def filterSinogram(sinogram, test=0.1):
    for i in range(sinogram.shape[0]):
        sinogram[i] = filterLine(sinogram[i], test=test)
    return sinogram

## filter une ligne (projection) via FFT
def filterLine(projection,test):
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
    # fft_signal_filtered = np.abs(fft_signal_filtered)

    # # Appliquer un filtre passe-haut
    # indices = np.arange(fft_signal_filtered.shape[0])
    # cut_off = int(len(projection)*test)
    # print(cut_off)

    # indices[indices < cut_off] = 0
    # indices[indices > 0] = 1
    fft_signal_filtered = fft_signal_filtered*ramp_filter


    return np.fft.ifft(np.fft.ifftshift(fft_signal_filtered)).real
