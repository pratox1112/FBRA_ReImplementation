# fbra/forward.py
from fbra.nn_bounds import nn_forward_box

def forward_reach(X0, model, plant, T):
    R = [[X0]]
    for t in range(T):
        next_boxes = []
        for box in R[-1]:
            u_box = nn_forward_box(box, model)
            x_box = plant(box, u_box)
            next_boxes.append(x_box)
        R.append(next_boxes)
    return R
