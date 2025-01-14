from geometry.Rectangle import Rectangle
from geometry.Point import Point
from quadTree.quadTreeNode import quadTreeNode
from visualiser.visualiser import Visualiser
from time import sleep
import matplotlib.pyplot as plt


class quadTree:

    def __init__(self, points: list[Point], maxPoints: int, vis=False):

        assert len(points) > 0, "Quad tree cannot be empty"

        self.maxPoints = maxPoints
        self.root: quadTreeNode = None

        if not vis:
            self.__buildTree(points)

    def draw(self, vis: Visualiser):
        self.root.draw(vis)

    def __findBorders(self, points) -> tuple[Point]:
        lowerLeft: Point = points[0]
        upperRight: Point = points[0]

        for point in points:
            lowerLeft = lowerLeft.lowerLeft(point)
            upperRight = upperRight.upperRight(point)

        return lowerLeft, upperRight

    def __buildTree(self, points):
        lowerLeft, upperRight = self.__findBorders(points)

        rootRectangle = Rectangle(lowerLeft, upperRight)

        self.root = quadTreeNode(self.maxPoints, rootRectangle)

        for point in points:
            self.root.insert(point)

    def search(self, rect: Rectangle) -> list[Point]:
        return self.root.search(rect)

    def searchVis(self, rect: Rectangle, vis: Visualiser):
        return self.root.searchVis(rect, vis, lw=2)

    def buildTreeVis(self, points, vis: Visualiser):
        lowerLeft, upperRight = self.__findBorders(points)

        rootRectangle = Rectangle(lowerLeft, upperRight)

        vis.drawRectangle(rootRectangle)

        self.root = quadTreeNode(self.maxPoints, rootRectangle)

        for point in points:
            currentPoint = vis.drawPoints(point, color='purple', markersize=10)
            sleep(vis.interval.get())
            self.root.insertVis(point, vis, 2)
            currentPoint.remove()
            currentPoint = vis.drawPoints(point)
            sleep(vis.interval.get())
