import numpy as np
import matplotlib.pyplot as plt

def ShowImage(image: np.ndarray, title: str, showColorBar: bool = False) -> None:
    
    fig = plt.figure(figsize = (20, 20))

    ax : plt.Axes = fig.add_subplot(111)

    fig.suptitle(title)

    im = ax.imshow(image)

    if showColorBar:
        plt.colorbar(im, ax = ax)

    plt.show()

def WriteImage(image: np.ndarray, outputPath: str = None) -> None:

    plt.imshow(image)

    plt.savefig(outputPath, dpi = 1200)