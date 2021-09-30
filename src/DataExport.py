import numpy as np
import pandas as pd
import Plant
import geojson

def PlantsExport(plants: np.ndarray, outputPath : str) -> None:

    dataFrame = pd.DataFrame.from_dict({
        "#" : [plant.Index for plant in plants],
        "Shape" : [f"{plant.Shape[0]}x{plant.Shape[1]}" for plant in plants],
        "Center" : [f"{plant.Center[0]}x{plant.Center[1]}" for plant in plants],
        "FieldColumn" : [plant.Column for plant in plants]
    })

    dataFrame.set_index("#", inplace = True)

    dataFrame.to_csv(outputPath)

def ColumnsExport(columns: np.ndarray, outputPath : str) -> None:

    dataFrame = pd.DataFrame.from_dict({
        "#" : [column.ColumnNumber for column in columns],
        "LeftBorder" : [column.LeftBorder for column in columns],
        "RightBorder" : [column.RightBorder for column in columns],
        "PlantsCount" : [column.PlantsCount for column in columns]
    })

    dataFrame.set_index("#", inplace = True)

    dataFrame.to_csv(outputPath)

def ExportCentersToGeoJson(plantsCenters: np.ndarray, outPath: str) -> None:
    
    features = []

    for n, center in enumerate(plantsCenters):
        x,y = center
        point = geojson.Point((x, y))

        features.append(geojson.Feature(geometry=point, properties={"#": n}))

    feature_collection = geojson.FeatureCollection(features)

    with open(outPath, 'w') as f:
        geojson.dump(feature_collection, f)
