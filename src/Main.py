import RasterioHandler
import ImageHandler
import VisualizeImage
import DataExport

def Main():

    filePath = "sources/imageSource.tif"

    red, green, blue, _ = RasterioHandler.ReadBands(filePath)

    image = RasterioHandler.CalculateVARI(red, green, blue)

    #VisualizeImage.ShowImage(ImageHandler.SetRandomIndex(image), "VARI")

    image = RasterioHandler.CleanVARI(image, 7, 50)

    #RasterioHandler.WriteFile(image, "output/outputVARI.tif", RasterioHandler.GetMeta(filePath))

    image = ImageHandler.ConvertToBitMask(image)

    #VisualizeImage.ShowImage(ImageHandler.SetRandomIndex(image), "Clear VARI")

    image = ImageHandler.RemoveGarbage(image)

    #VisualizeImage.ShowImage(ImageHandler.SetRandomIndex(image), "Remove garbage")

    image = ImageHandler.SplitGroup(image)

    #RasterioHandler.WriteFile(ImageHandler.ConvertFromBitMask(image), "output/outputSplit.tif", RasterioHandler.GetMeta(filePath))

    #VisualizeImage.ShowImage(ImageHandler.SetUniqueIndex(image), "Split", True)

    plants = ImageHandler.FindPlants(image)
    columns = ImageHandler.FindColumns(image)

    print(f"Found {len(plants)} plants")

    VisualizeImage.ShowPlants(ImageHandler.ConvertFromBitMask(image), plants, columns = columns, showBorder = True)

    DataExport.PlantsExport(plants, "output/plants.csv")
    DataExport.ColumnsExport(columns, "output/columns.csv")

if __name__ == "__main__":
    Main()    