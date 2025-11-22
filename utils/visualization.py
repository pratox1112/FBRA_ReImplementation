# utils/visualization.py
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
