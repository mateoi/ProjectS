#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 16:15:34 2017

@author: mateo
"""

from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
from numpy.fft import fft, fftfreq


def read_info_file(filename):
    """
    Reads the given filename and returns the data as integers in a 1D numpy
    array.
    """
    with open(filename) as file:
        results = file.readlines()
    results = [int(line.strip()) for line in results]  # Remove any whitespace
    return np.array(results)


def simple_plot(data, **kwargs):
    """
    Returns a figure containing a simple plot of the given measurements.
    Extra keyword arguments are passed on to plt.plot().
    """
    plt.plot(data, **kwargs)
    plt.ylabel("CPU cycles per multiplication")
    plt.xlabel("Iterations")
    return plt.gcf()


def frequency_spectrum_plot(data, points=32, **kwargs):
    """
    Returns a figure containing the frequency spectrum of the given data.
    """
    frequencies, power_spectrum = calculate_frequency_spectrum(data, points)
    width = frequencies[1] - frequencies[0]
    color = np.linspace(0, 1, points)
    color = plt.cm.viridis(colors)
    plt.bar(frequencies, power_spectrum, width=width, color=color, **kwargs)
    plt.xlabel("Frequency band")
    plt.ylabel("Intensity")
    return plt.gcf()


def spectrogram(data, window_size=500, points=32, peak_scaling=1,
                linthresh=0.1, **kwargs):
    """
    Returns a figure containing a spectrogram of the given data in windows of
    the supplied window size. The color scale is logarithmic, to best show
    differences, and the maximum is clipped by a factor of peak_scaling.
    """
    matrix = calculate_spectrogram_matrix(data, window_size, points)
    aspect_ratio = matrix.shape[0] / matrix.shape[1]
    norm = colors.SymLogNorm(linthresh=linthresh, vmin=matrix.min(),
                             vmax=matrix.max() / peak_scaling)
    plt.matshow(matrix.T, aspect=aspect_ratio, norm=norm, **kwargs)
    plt.ylabel("Frequency band")
    plt.xlabel("Iterations")
    return plt.gcf()



def calculate_spectrogram_matrix(data, window_size, points):
    """
    Calculates a spectrogram matrix of the power spectrum of the given data
    with a sliding window size of window_size and the given number of frequency
    bands.
    """
    matrix = []
    for i in range(len(data) - window_size):
        window = data[i:i + window_size]
        matrix += calculate_frequency_spectrum(window, points)
    return np.array(matrix)


def calculate_frequency_spectrum(data, points):
    """
    Calculates the frequency spectrum of the given data at the given number of
    data points. Returns a tuple of the ordered frequencies and the
    corresponding powers.
    """
    power_spectrum = np.abs(fft(data)) ** 2
    frequencies = fftfreq(points)
    indices = np.argsort(frequencies)
    return frequencies[indices], power_spectrum[indices]
