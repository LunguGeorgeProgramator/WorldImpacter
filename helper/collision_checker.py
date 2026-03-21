import math


class ColisionChecler:

    def __init__(self):
        pass

    def colision_detection(self, c1, c2):
        x1, y1, r1 = c1
        x2, y2, r2 = c2
        distance = math.hypot(x2 - x1, y2 - y1)
        return distance <= (r1 + r2)