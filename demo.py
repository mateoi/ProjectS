#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 10:48:23 2017

@author: mateo
"""

import subprocess
import fileinput
import sys
from matplotlib import pyplot as plt

BIN_NAME = "Release/CycleCounter_Windows.exe"


def __main__():
    if sys.platform == "win32":
        if len(sys.argv) >= 2:
            iterations = int(sys.argv[1])
        else:
            iterations = 2000
        output = get_stdout(iterations)
        ints = to_ints(output)
    else:
        output = read_stdin()
        ints = [int(line) for line in output]

    plt.plot(ints)
    plt.ylabel("CPU cycles per multiplication")
    plt.xlabel("Iterations")
    # plt.gca().set_ylim(bottom=0)
    plt.show()


def to_ints(string):
    """
    Converts a newline-separated string into a list of ints
    """
    as_list = string.splitlines()
    return [int(item) for item in as_list]


def get_stdout(iterations):
    """
    Executes the cycle counter and returns the standard output.
    """
    args = (BIN_NAME, str(iterations))
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    return output.decode("utf-8")


def read_stdin():
    return [line for line in fileinput.input()]


__main__()
