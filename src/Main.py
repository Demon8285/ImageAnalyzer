import RasterioHandler
import ImageHandler
import VisualizeImage
import DataExport

import rasterio
import rasterio.transform

def Main():

    filePath = "sources/imageSource.tif"

    red, green, blue, _ = RasterioHandler.ReadBands(filePath)
    meta = RasterioHandler.GetMeta(filePath)

    image = RasterioHandler.CalculateVARI(red, green, blue)

    #VisualizeImage.ShowImage(ImageHandler.SetRandomIndex(image), "VARI")

    image = RasterioHandler.CleanVARI(image, 7, 50)

    #RasterioHandler.WriteFile(image, "output/outputVARI.tif", meta)

    image = ImageHandler.ConvertToBitMask(image)

    #VisualizeImage.ShowImage(ImageHandler.SetRandomIndex(image), "Clear VARI")

    image = ImageHandler.RemoveGarbage(image)

    #VisualizeImage.ShowImage(ImageHandler.SetRandomIndex(image), "Remove garbage")

    image = ImageHandler.SplitGroup(image)

    #RasterioHandler.WriteFile(ImageHandler.ConvertFromBitMask(image), "output/outputSplit.tif", meta)

    #VisualizeImage.ShowImage(ImageHandler.SetUniqueIndex(image), "Split", True)
    #VisualizeImage.WriteImage(ImageHandler.SetUniqueIndex(image), outputPath = "output/SplitColor.png")

    plants = ImageHandler.FindPlants(image)
    columns = ImageHandler.FindColumns(image)

    print(f"Found {len(plants)} plants")

    plantsMap = ImageHandler.DrawPlants(ImageHandler.ConvertFromBitMask(image), plants, columns, showBorder = True)
    #RasterioHandler.WriteMultiplyChannelsFile(plantsMap, "output/PlantsMap.tif", meta)

    #VisualizeImage.ShowImage(plantsMap, "Plant Map")

    #DataExport.PlantsExport(plants, "output/plants.csv")
    #DataExport.ColumnsExport(columns, "output/columns.csv")

    #columnsImage = ImageHandler.DrawColumns(image, columns)
    #RasterioHandler.WriteFile(ImageHandler.ConvertFromBitMask(columnsImage), "output/columnsMap.tif", meta)

    DataExport.ExportCentersToGeoJson(RasterioHandler.ConvertCenters(plants, filePath), "output/PlantCenters.geojson")

if __name__ == "__main__":
    Main()    