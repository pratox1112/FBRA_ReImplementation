# fbra/backward.py
from utils.sampling import sample_box
from fbra.boxes import Box
import numpy as np

def backward_step(R_fb_t, R_f_tminus1, model, plant, samples=200):
    result = []
    for fb in R_fb_t:

        xs = sample_box(R_f_tminus1, samples)
        keep = []

        for x in xs:
            u = model(x).detach().numpy()
            next_box = plant(Box(x, x), Box(u, u))
            if fb.intersect(next_box):
                keep.append(x)

        if keep:
            keep = np.array(keep)
            result.append(Box(keep.min(axis=0), keep.max(axis=0)))

    return result
