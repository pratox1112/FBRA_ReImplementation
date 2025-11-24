# utils/visualization.py

import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import matplotlib.pyplot as plt
from fbra.boxes import Box

def plot_boxes(boxes, color="blue", alpha=0.25, label=None):
    """
    Plot 2D boxes for visualization.
    """
    for b in boxes:
        x1, x2 = b.low
        X1, X2 = b.up
        plt.fill([x1, X1, X1, x1],
                 [x2, x2, X2, X2],
                 color=color, alpha=alpha, label=label)

def plot_initial_and_unsafe(X0, Unsafe):
    plot_boxes([X0], color="green", alpha=0.3, label="Initial")
    plot_boxes([Unsafe], color="red", alpha=0.3, label="Unsafe")

    plt.legend()
    plt.xlabel("State 1")
    plt.ylabel("State 2")
    plt.title("Initial and Unsafe Sets")

def plot_three_stages(R1, R2, R3, unsafe):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(18,6))
    stages = [
        ("Forward Reachability Only", R1),
        ("After Forward Refinement", R2),
        ("After Backward Refinement (Final)", R3)
    ]

    for ax, (title, R) in zip(axes, stages):
        for t, boxes in R.items():
            for b in boxes:
                low = b.low
                up = b.up
                ax.add_patch(
                    plt.Rectangle(
                        (low[0], low[1]),
                        up[0] - low[0],
                        up[1] - low[1],
                        fill=True,
                        color="blue",
                        alpha=0.15
                    )
                )

        # unsafe region
        low = unsafe.low
        up = unsafe.up
        ax.add_patch(
            plt.Rectangle(
                (low[0], low[1]),
                up[0] - low[0],
                up[1] - low[1],
                fill=True,
                color="red",
                alpha=0.3
            )
        )

        ax.set_title(title)
        ax.set_xlabel("x1")
        ax.set_ylabel("x2")
        ax.grid(True)
        ax.axis("equal")

    plt.tight_layout()
    plt.show()

