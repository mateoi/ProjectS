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


def frequency_spectrum_plot(data, points=None, **kwargs):
    """
    Returns a figure containing the frequency spectrum of the given data.
    """
    power_spectrum = np.abs(fft(data)) ** 2
    points = data.size if points is None else points
    frequencies = fftfreq(points)
    indices = np.argsort(frequencies)
    width = frequencies[indices][1] - frequencies[indices][0]
    colors = np.linspace(0,1, points)
    colors = plt.cm.viridis(colors)
    plt.bar(frequencies[indices], power_spectrum[indices], width=width,
            color=colors)
    return plt.gcf()
