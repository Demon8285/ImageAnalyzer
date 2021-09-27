import Plant
import numpy as np
import matplotlib.pyplot as plt
import cv2

def ShowImage(image: np.ndarray, title: str, showColorBar: bool = False) -> None:
    
    fig = plt.figure(figsize = (20, 20))

    ax : plt.Axes = fig.add_subplot(111)

    fig.suptitle(title)

    im = ax.imshow(image)

    if showColorBar:
        plt.colorbar(im, ax = ax)

    plt.show()

def ShowPlants(image: np.ndarray, plants: np.ndarray, outputPath: str = None, columns = None, showBorder: bool = False) -> None:

    color = (255, 0, 0)

    if columns is not None:
        for column in columns:
            image[:, column.LeftBorder] = 255

    image = image.astype(np.uint8)

    image = cv2.merge((image, image, image))

    for plant in plants:
        
        if showBorder: image = cv2.circle(image, plant.Center, plant.GetDiagonal(), color)
        image = cv2.circle(image, plant.Center, 1, color, -1)

    fig = plt.figure()

    ax : plt.Axes = fig.add_subplot(111)

    fig.suptitle("Plants")

    ax.imshow(image)

    if outputPath is not None:
        plt.savefig(outputPath, dpi = 1000)

    plt.show()

def ShowColumns(image: np.ndarray, columns: np.ndarray) -> None:

    for column in columns:
        image[:, column.LeftBorder] = 2
    
    ShowImage(image, "Columns")