import numpy as np


def generate_fake_elevation(rows=20, cols=20):
    # simulate terrain
    elevation = np.random.rand(rows, cols) * 100
    return elevation