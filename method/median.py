import numpy as np

from video import pixels, X, frames



def weighted_median(values, weights):
    # On trie les valeurs par ordre croissant
    # en gardant les poids correspondants
    values = np.asarray(values)
    weights = np.asarray(weights)

    sort_idx = np.argsort(values)
    v = values[sort_idx]
    w = weights[sort_idx]

    # On calcule la médiane pondérée
    cum_w = np.cumsum(w)
    cutoff = np.sum(w) / 2
    index = np.searchsorted(cum_w, cutoff)
    return v[index]

def median_compute_b(X, a=None):
    if a is None:
        a = [1.0] * frames

    b = [1.0] * pixels

    for i in range(pixels):
        b[i] = weighted_median(X[i,:], a)

    return b




def median_compute_a(X, b):
    a = np.zeros(frames)
    for frame in range(frames):
        y = X[:, frame] / b
        w = np.abs(b)
        a[frame] = weighted_median(y, w)

    return a