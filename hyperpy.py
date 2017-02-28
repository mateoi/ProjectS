#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 16:15:34 2017

@author: mateo
"""

from matplotlib import pyplot as plt
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


def frequency_spectrum_plot(data, **kwargs):
    """
    Returns a figure containing the frequency spectrum of the given data.
    """
    power_spectrum = np.abs(fft(data)) ** 2
    frequencies = fftfreq(data.size)
    indices = np.argsort(frequencies)
    plt.plot(frequencies[indices], power_spectrum[indices])
    return plt.gcf()
