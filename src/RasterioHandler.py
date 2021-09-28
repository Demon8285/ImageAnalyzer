from ast import Str
from typing import List
import numpy as np
import rasterio as rast

def ReadBands(filePath: str) -> List[np.ndarray]:
    
    with rast.open(filePath) as image:

        return [band for band in image.read()]

def GetMeta(filePath: str) -> dict:

    with rast.open(filePath) as image:
        return image.meta

def CalculateVARI(red: np.ndarray, green: np.ndarray, blue : np.ndarray) -> np.ndarray:
    
    np.seterr(divide='ignore', invalid='ignore')

    return (((green - red) / (green + red - blue)) * 100).astype(np.uint8)

def CleanVARI(image: np.ndarray, minVari: float, maxVari: float) -> np.ndarray:

    image[(image > minVari) & (image < maxVari)] = 255
    image[image != 255] = 0

    return image

def WriteFile(image: np.ndarray, outputPath: str, meta: dict) -> None:

    meta.update(dtype = rast.uint8, driver = 'GTiff', count = 1)

    with rast.open(outputPath, 'w', **meta) as dst:
        dst.write(image, indexes = 1)

def WriteMultiplyChannelsFile(image: np.ndarray, outputPath: str, meta: dict) -> None:

    meta.update(dtype = rast.uint8, driver = 'GTiff', count = 3)

    with rast.open(outputPath, 'w', **meta) as dst:
        dst.write(np.rollaxis(image, axis = 2))
