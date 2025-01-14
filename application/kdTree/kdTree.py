from geometry.Point import Point
from kdTree.QuickSelect import quickSelect
from geometry.Rectangle import Rectangle
from math import inf
from kdTree.kdTreeNode import kdTreeNode
from visualiser.visualiser import Visualiser
from time import sleep


class kdTree:
    def __init__(self, points: list[Point], vis=False):
        assert len(points) > 0, 'KD-Tree cannot be initialized as empty'
        self.dim = points[0].dim
        assert all(
            point.dim == self.dim for point in points), 'Points must have same number of dimensions'

        if not vis:
            self.root = self.__buildTree(points)

    def __buildTree(self, points):
        def buildTreeRec(points: list[Point], l: int, r: int, rect: Rectangle, dim: int):
            if l > r:
                return None
            if l == r:
                return points[l]
            mid = (l+r)//2
            midPoint = quickSelect(points, l, r, mid, dim)
            newNode = kdTreeNode(midPoint.get_dim(
                dim), dim, rect, points[l:r+1])
            rectLeft, rectRight = rect.divideRectIntoTwo(
                dim, midPoint.get_dim(dim))
            newNode.left = buildTreeRec(
                points, l, mid, rectLeft, (dim+1) % self.dim)
            newNode.right = buildTreeRec(
                points, mid+1, r, rectRight, (dim+1) % self.dim)
            return newNode
        lowerLeft, upperRight = Point((inf, inf)), Point((-inf, -inf))
        for point in points:
            lowerLeft = lowerLeft.lowerLeft(point)
            upperRight = upperRight.upperRight(point)
        rectStart = Rectangle(lowerLeft, upperRight)
        return buildTreeRec(points, 0, len(points)-1, rectStart, 0)

    def search(self, rectangle: Rectangle):

        def searchKD(p, rect: Rectangle):
            if isinstance(p, Point):
                if rect.containsPoint(p):
                    return [p]
            elif rect.containsRect(p.rect):
                return p.allLeaves()
            elif rectangle.intersects(p.rect):
                res = []
                res += searchKD(p.left, rect)
                res += searchKD(p.right, rect)
                return res
            return []
        return searchKD(self.root, rectangle)

    def countKD(self, rectangle: Rectangle):
        def count(p, rect: Rectangle):
            if isinstance(p, Point):
                if rect.containsPoint(p):
                    return 1
            elif rect.containsRect(p.rect):
                return p.countLeaves()
            elif rectangle.intersects(p.rect):
                res = 0
                res += count(p.left, rect)
                res += count(p.right, rect)
                return res
            return 0
        return count(self.root, rectangle)

    def draw(self, vis: Visualiser):
        self.root.draw(vis, lw=2)

    def buildTreeVis(self, points, vis: Visualiser):
        def buildTreeRec(points: list[Point], l: int, r: int, rect: Rectangle, dim: int, vis: Visualiser, lw=2):
            if l > r:
                return None
            if l == r:
                return points[l]
            pointsVis = vis.drawPointsList(
                points[l:r+1], color='purple', markersize=9)
            sleep(vis.interval.get())
            mid = (l+r)//2
            midPoint = quickSelect(points, l, r, mid, dim)
            sleep(vis.interval.get())
            pointVis = vis.drawPoints(midPoint, color='cyan', markersize=11)
            sleep(vis.interval.get())
            newNode = kdTreeNode(midPoint.get_dim(
                dim), dim, rect, points[l:r+1])
            vis.drawLineInRect2D(newNode.rect, newNode.axis, newNode.dim, lw)
            sleep(vis.interval.get())
            pointVis.remove()
            vis.removePointsList(pointsVis)
            sleep(vis.interval.get())
            rectLeft, rectRight = rect.divideRectIntoTwo(
                dim, midPoint.get_dim(dim))
            newNode.left = buildTreeRec(
                points, l, mid, rectLeft, (dim+1) % self.dim, vis, lw*4/5)
            newNode.right = buildTreeRec(
                points, mid+1, r, rectRight, (dim+1) % self.dim, vis, lw*4/5)
            return newNode
        vis.drawPoints(points)
        lowerLeft, upperRight = Point((inf, inf)), Point((-inf, -inf))
        for point in points:
            lowerLeft = lowerLeft.lowerLeft(point)
            upperRight = upperRight.upperRight(point)
        rectStart = Rectangle(lowerLeft, upperRight)
        return buildTreeRec(points, 0, len(points)-1, rectStart, 0, vis)

    def searchVis(self, rectangle: Rectangle, vis: Visualiser):
        def searchKD(p, rect: Rectangle, vis):
            if isinstance(p, Point):
                if rect.containsPoint(p):
                    vis.drawPoints(p, color='cyan', markersize=7)
                    sleep(vis.interval.get())
                    return [p]
            elif rect.containsRect(p.rect):
                rectVis = vis.drawRectangle(p.rect, c='green', lw=2)
                res = p.allLeaves()
                vis.drawPoints(res, color='green', markersize=7)
                sleep(vis.interval.get())
                rectVis.remove()
                sleep(vis.interval.get())
                return res
            elif rectangle.intersects(p.rect):
                rectVis = vis.drawRectangle(p.rect, c='brown', lw=2)
                sleep(vis.interval.get())
                rectVis.remove()
                sleep(vis.interval.get())
                res = []
                res += searchKD(p.left, rect, vis)
                res += searchKD(p.right, rect, vis)
                return res
            return []
        return searchKD(self.root, rectangle, vis)
