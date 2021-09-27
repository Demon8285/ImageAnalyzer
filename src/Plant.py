
from typing import Tuple


class Plant(object):

    def __init__(self, index : int, shape: Tuple[int, int], center: Tuple[int, int], column: int) -> None:
        self.Index = index
        self.Shape = shape
        self.Center = center
        self.Column = column 

    def GetDiagonal(self) -> float:
        return int((self.Shape[0] ** 2 + self.Shape[1] ** 2) ** 0.5) // 2

class Column(object):

    def __init__(self, columnNumber: int, leftBorder: int, rightBorder: int, plantsCount: int) -> None:
        self.ColumnNumber = columnNumber
        self.LeftBorder = leftBorder
        self.RightBorder = rightBorder
        self.PlantsCount = plantsCount