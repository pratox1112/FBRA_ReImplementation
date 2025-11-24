# fbra/verifier.py

import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from fbra.forward import forward_reach
from fbra.refine_forward import refine_forward_boxes
from fbra.backward import backward_step
from fbra.boxes import Box
from utils.merge import merge_box_list

def intersects_any(boxes, region):
    return any(b.intersect(region) for b in boxes)

def contains_any(boxes, region):
    return any(region.contains(b) for b in boxes)

def verify(X0, model, plant, unsafe, T):
    R_f = forward_reach(X0, model, plant, T)

    for t in range(1, T+1):

        # classification
        safe = True
        unknown = False

        for b in R_f[t]:
            if unsafe.contains(b):
                return "Unsafe"
            if unsafe.intersect(b):
                unknown = True
                safe = False

        if safe:
            continue

        if unknown:
            # refine forward boxes at time t
            R_f[t] = refine_forward_boxes(R_f[t], unsafe)

            # backward init
            R_b = {t: R_f[t]}

            for k in reversed(range(t)):
                merged = merge_box_list(R_f[k])
                R_b[k] = backward_step(R_b[k+1], merged, model, plant)

            for b in R_b[0]:
                if b.intersect(X0):
                    return "Unsafe"

            # re-run forward after refinement
            R_f = forward_reach(X0, model, plant, T)

    return "Safe"
