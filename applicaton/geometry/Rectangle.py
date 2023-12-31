from geometry.Point import Point


class Rectangle:  # jeszcze nieprzydatne ale moze mi sie przyda do jakiejs wizualizacji czy cos
    def __init__(self, point1: Point, point2: Point) -> None:
        self.lowerLeft = point1.lowerLeft(point2)
        self.upperRight = point1.upperRight(point2)
        self.dim = point1.dim

    def __str__(self):
        return str(self.lowerLeft) + ' - ' + str(self.upperRight)

    def intersects(self, other):
        return self.lowerLeft.precedes(other.upperRight) and self.upperRight.follows(other.lowerLeft)

    def containsPoint(self, point: Point):
        return point.follows(self.lowerLeft) and point.precedes(self.upperRight)

    def draw(self, ax, c='k', lw=1, **kwargs):
        x1, y1 = self.lowerLeft.x(), self.lowerLeft.y()
        x2, y2 = self.upperRight.x(), self.upperRight.y()
        ax.plot([x1, x2, x2, x1, x1],
                [y1, y1, y2, y2, y1], c=c, lw=lw, **kwargs)

    def containsRect(self, other):
        return other.lowerLeft.follows(self.lowerLeft) and other.upperRight.precedes(self.upperRight)

    def divideRectIntoTwo(self, dim, divLine):
        Lower = self.lowerLeft.data
        Upper = self.upperRight.data
        assert divLine <= Upper[dim] or divLine >= Lower[dim], 'Line does not belong to rectangle'
        lowerIntersection, upperIntersection = list(
            Lower), list(Upper)
        lowerIntersection[dim] = upperIntersection[dim] = divLine
        lowerIntersection, upperIntersection = tuple(
            lowerIntersection), tuple(upperIntersection)
        return (Rectangle(Point(Lower), Point(upperIntersection)), Rectangle(Point(lowerIntersection), Point(Upper)))

    def drawLineInRect2D(self, ax, line, dim, lw=3.0, c='k'):
        if dim == 0:
            y1, y2 = self.lowerLeft.y(), self.upperRight.y()
            ax.plot([line, line], [y1, y2], c, linewidth=lw)
        if dim == 1:
            x1, x2 = self.lowerLeft.x(), self.upperRight.x()
            ax.plot([x1, x2], [line, line], c, linewidth=lw)