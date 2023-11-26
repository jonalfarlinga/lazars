import math
from constants import *


def deg_to_vector(deg):
    unit_vector = (
        math.cos((deg * math.pi)/180),
        math.sin((deg * math.pi)/180)
    )
    return unit_vector


def distance(point1, point2):
    distance = math.sqrt(
            (point1[0] - point2[0]) ** 2 +
            (point1[1] - point2[1]) ** 2
    )
    return distance


# returns y2
def linear_eq(source, x2, unit_vector):
    x1, y1 = source
    uvx, uvy = unit_vector
    return y1 + ((x2 - x1) / uvx * uvy)


def linear_eq_inv(source, y2, unit_vector):
    x1, y1 = source
    uvx, uvy = unit_vector
    return x1 + ((y2 - y1) / uvy * uvx)


def round(num):
    test = num * 10
    if test % 10 >= 5:
        return math.ceil(num)
    else:
        return math.floor(num)


def calculate_line(source, deg, rects):
    line_segments = []
    while source:
        bounce = None
        uv = deg_to_vector(deg)
        if deg > 315 or deg < 45:
            for x2 in range(source[0]+1, SCREEN_WIDTH):
                y2 = round(
                    linear_eq(source, x2, uv)
                )
                for rect in rects:
                    if rect.collidepoint((x2, y2)):
                        bounce = ((x2, y2))
                        break
                if bounce:
                    break
        elif 135 < deg < 225:
            for x2 in reversed(range(0, source[0]-1)):
                y2 = round(
                    linear_eq(source, x2, uv)
                )
                for rect in rects:
                    if rect.collidepoint((x2, y2)):
                        bounce = ((x2, y2))
                        break
                if bounce:
                    break
        elif 45 <= deg <= 135:
            for y2 in range(source[1]+1, SCREEN_HEIGHT):
                x2 = round(
                    linear_eq_inv(source, y2, uv)
                )
                for rect in rects:
                    if rect.collidepoint((x2, y2)):
                        bounce = ((x2, y2))
                        break
                if bounce:
                    break
        elif 225 <= deg <= 315:
            for y2 in reversed(range(0, source[1]-1)):
                x2 = round(
                    linear_eq_inv(source, y2, uv)
                )
                for rect in rects:
                    if rect.collidepoint((x2, y2)):
                        bounce = ((x2, y2))
                        break
                if bounce:
                    break


        line_segments.append((source, bounce))
        if bounce:
            source = bounce

        # else:
        source = None  # simplify for now
    return line_segments
