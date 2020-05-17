#simple imports
import json
from requests import get, post
from requests import Response
import numpy as np
import numpy as np2

#imports with submodules
import scipy.stats
from scipy import fft
from scipy.linalg import hilbert
from scipy.optimize import nonlin
import matplotlib.pyplot as plt

json.loads("{}")
get("http://ya.ru")


def f():
    post("http://google.com")


def g():
    import os
    os.mkdir("tmp")

a = np.ones(10)
b = np2.zeros(10)
c = scipy.stats.alpha(1)
f = fft.ifft
n = nonlin.newton_krylov
h = hilbert(2)

plt.plot(a, b)