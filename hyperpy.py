#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 16:15:34 2017

@author: mateo
"""

import subprocess
from os import sys
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
from numpy.fft import fft, fftfreq

if sys.platform == "win32":
    BIN_NAME = "bin/CycleCounter_Windows.exe"
else:
    BIN_NAME = "bin/linux_count_cycles"


def read_info_file(filename):
    """
    Reads the given filename and returns the data as integers in a 1D numpy
    array.
    """
    with open(filename) as file:
        results = file.readlines()
    results = [int(line.strip()) for line in results]  # Remove any whitespace
    return np.array(results)


def scan_hyperthreading_delay(iterations=1000):
    """
    Runs the hyperthreading attach for the given number of iterations and
    returns a numpy array containing the results.
    """
    output = subprocess.check_output([BIN_NAME, str(iterations)])
    lines = [line.strip() for line in output.splitlines()]
    return np.array([int(line) for line in lines])


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
    color = plt.cm.viridis(color)
    plt.bar(frequencies, power_spectrum, width=width, color=color, **kwargs)
    plt.xlabel("Frequency band")
    plt.ylabel("Intensity")
    return plt.gcf()


def spectrogram(data, window_size=500, points=32, peak_scaling=1,
                linthresh=0.1, blinding=False, **kwargs):
    """
    Returns a figure containing a spectrogram of the given data in windows of
    the supplied window size. The color scale is logarithmic, to best show
    differences, and the maximum is clipped by a factor of peak_scaling.
    The data may be blinded, which blocks out the dominant frequency.

    Extra arguments (like colormap) are passed on to plt.matshow.
    """
    if len(data.shape) == 1:
        matrix = calculate_spectrogram_matrix(data, window_size, points,
                                              blinding)
    else:
        matrix = data
    aspect_ratio = 0.7 * matrix.shape[0] / matrix.shape[1]
    norm = colors.SymLogNorm(linthresh=linthresh, vmin=matrix.min(),
                             vmax=matrix.max() / peak_scaling)
    plt.matshow(matrix.T, aspect=aspect_ratio, norm=norm, **kwargs)
    plt.ylabel("Frequency band")
    plt.xlabel("Iterations")
    return plt.gcf()


def calculate_spectrogram_matrix(data, window_size, points, blinding=False):
    """
    Calculates a spectrogram matrix of the power spectrum of the given data
    with a sliding window size of window_size and the given number of frequency
    bands.
    """
    matrix = np.empty((len(data) - window_size, points))
    for i in range(len(data) - window_size):
        window = data[i:i + window_size]
        spectrum = calculate_frequency_spectrum(window, points)[1]
        matrix[i] = spectrum
    matrix = np.array(matrix)
    if blinding:
        middle = points // 2
        matrix[:, middle] = np.zeros(matrix.shape[0])
    return matrix


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


def hamming_distance(array1, array2):
    """
    Calculates the hamming distance between the two arrays
    """
    min_index = min(array1.size, array2.size)
    equal_indices = np.equal(array1[:min_index], array2[:min_index])
    return min_index - np.count_nonzero(equal_indices)


def differentiate_arrays(array1, array2, window=100, max_slide=10,
                         differential_function=hamming_distance):
    """
    Calculates the difference between the two arrays (array1 - array2), while
    adjusting the arrays linearly in windows of the given size and with a given
    maximum slide, in order to minimize the given differential function.
    """
    index1 = 0
    index2 = 0
    result = np.array([])
    while index1 < array1.size and index2 < array2.size:
        slide = _minimize_difference(array1[index1:index1 + window],
                                     array2[index2:index2 + window], max_slide,
                                     differential_function)
        if slide > 0:
            slice1 = array1[index1 + slide:index1 + window]
            slice2 = array2[index2:index2 + window - slide]
            min_index = min(slice1.size, slice2.size)
            result = np.append(result, slice1[:min_index] - slice2[:min_index])
            index1 += window
            index2 += window - slide
        else:
            slice1 = array1[index1:index1 + window - slide]
            slice2 = array2[index2 + slide:index2 + window]
            min_index = min(slice1.size, slice2.size)
            result = np.append(result, slice1[:min_index] - slice2[:min_index])
            index1 += window - slide
            index2 += window
    return result


def _minimize_difference(array1, array2, max_slide,
                         differential_function=hamming_distance):
    """
    Calculates the slide (less than or equal to max_slide) that will result in
    the differential function being minimized for the two arrays. A slide is an
    offset of array1 with respect to array2: a slide of 5, for example, means
    that the function is minimized for array1[5:] and array2[:-5]; a slide of
    -3 means that the function is minimized for array1[:-3] and array2[3:].
    """
    minimum = (0, differential_function(array1, array2))
    for i in range(1, max_slide + 1):
        diff_r = differential_function(array1[i:], array2[:-i])
        diff_l = differential_function(array1[:-i], array2[i:])
        if diff_r < minimum[1]:
            minimum = (i, diff_r)
        if diff_l < minimum[1]:
            minimum = (-i, diff_l)
        return minimum[0]
