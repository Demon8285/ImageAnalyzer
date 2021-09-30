import Plant
import random
import numpy as np
from scipy import ndimage
import math
import cv2


def ConvertToBitMask(image: np.ndarray) -> np.ndarray:

    return np.where(image > 0, 1, 0)

def ConvertFromBitMask(image: np.ndarray) -> np.ndarray:

    return np.where(image == 1, 255, 0)   

def RemoveGarbage(image: np.ndarray, cutValue : float = None) -> np.ndarray:

    labels, _ = ndimage.label(image)
    things = ndimage.find_objects(labels)

    shapeSquare = lambda x: image[x].shape[0] * image[x].shape[1]

    thingsSquares = np.array([shapeSquare(thing) for thing in things])

    if cutValue is None:
        cutValue = np.mean(thingsSquares)

    for thing in things:
        if shapeSquare(thing) < cutValue:
            values = image[thing]
            values[values == 1] = 0
    
    return image

def SplitGroup(image: np.ndarray) -> np.ndarray:

    labels, _ = ndimage.label(image)
    things = ndimage.find_objects(labels)

    thingHeight = lambda x: image[x].shape[0]

    thingsHeight = np.array([thingHeight(x) for x in things])
    
    meanHeight = np.mean(thingsHeight)

    for thing in things:
        height = thingHeight(thing)

        if height > meanHeight * 2:
            chunksNumer = math.ceil(height / meanHeight)
            chunksLength = (height - 1) // chunksNumer 

            for chunk in range(1, chunksNumer + 1):
                if len(image[thing][chunksLength * chunk:]) < chunksLength:
                    break
                image[thing][chunksLength * chunk] = 0
        
    return(image)

def SetUniqueIndex(image: np.ndarray) -> np.ndarray:

    labels, _ = ndimage.label(image)

    return labels

def SetRandomIndex(image: np.ndarray) -> np.ndarray:

    newImage = np.copy(image)
    labels, _ = ndimage.label(newImage)
    things = ndimage.find_objects(labels)

    for thing in things:
        values = newImage[thing]
        values[values == 1] = random.randint(255, 5000)

    return newImage

def FindCenters(image: np.ndarray) -> np.ndarray:

    labels, n = ndimage.label(image)

    return ndimage.centers(image, labels, index = range(1, n + 1))

def FindPlants(image: np.ndarray) -> np.ndarray:

    plants = []

    labels, n = ndimage.label(image)
    centers = ndimage.center_of_mass(image, labels, index = range(1, n + 1))
    things = ndimage.find_objects(labels)

    thingWeight = lambda x: image[x].shape[1]

    thingsWeight = np.array([thingWeight(x) for x in things])

    meanWeight = np.mean(thingsWeight)
    stdWeight = np.std(thingsWeight)
    
    columnWeight = int((meanWeight + stdWeight) * 1.5)
    columnCount = image.shape[1] // columnWeight

    for index in range(n):
        center = (int(centers[index][1]), int(centers[index][0]))
        shape = image[things[index]].shape

        plant = Plant.Plant(index + 1, shape, center, (center[0] // columnWeight) + 1)
        plants.append(plant)

    return np.array(plants)

def FindColumns(image: np.ndarray) -> np.ndarray:

    columns = []

    labels, n = ndimage.label(image)
    centers = ndimage.center_of_mass(image, labels, index = range(1, n + 1))
    things = ndimage.find_objects(labels)
    thingsXPositions = np.array([int(center[1]) for center in centers])

    thingWeight = lambda x: image[x].shape[1]

    thingsWeight = np.array([thingWeight(x) for x in things])

    meanWeight = np.mean(thingsWeight)
    stdWeight = np.std(thingsWeight)
    
    fieldWeight = image.shape[1]
    columnWeight = int((meanWeight + stdWeight) * 1.5)
    columnCount =  fieldWeight // columnWeight

    for columnNumer in range(columnCount):
        left = columnWeight * columnNumer
        
        if columnNumer != columnCount - 1:
            right = columnWeight * (columnNumer + 1)
        else:
            right = fieldWeight
        
        plantsCount = len(thingsXPositions[(thingsXPositions >= left) & (thingsXPositions < right)])

        columns.append(Plant.Column(columnNumer + 1, left, right, plantsCount))

    return np.array(columns)

def DrawPlants(image: np.ndarray, plants: np.ndarray, columns: np.ndarray = None, showBorder: bool = False) -> np.ndarray:

    image = np.copy(image)

    color = (255, 0, 0)

    if columns is not None:
        for column in columns:
            image[:, column.LeftBorder] = 255

    image = image.astype(np.uint8)

    image = cv2.merge((image, image, image))

    for plant in plants:
        
        if showBorder: image = cv2.circle(image, plant.Center, plant.GetDiagonal(), color)
        image = cv2.circle(image, plant.Center, 1, color, -1)

    return image

def DrawColumns(image: np.ndarray, columns: np.ndarray) -> np.ndarray:
    
    image = np.zeros(image.shape)

    for column in columns:
        image[:, column.LeftBorder] = 1

    return image
        

