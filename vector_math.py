import pygame
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
            (point1[0] - point2[1]) ** 2 +
            (point1[0] - point2[1]) ** 2
    )


# returns y2
def linear_eq(source, x2, unit_vector):
    x1, y1 = source
    uvx, uvy = unit_vector
    return y1 + ((x2 - x1 / uvx) * uvy)


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
        x1, y1 = source
        uvx, uvy = deg_to_vector(deg)
        if uvx > 0:
            collisions = []
            for x2 in range(x1+1, SCREEN_WIDTH):
                y2 = round(
                    y1 + ((x2 - x1) / uvx * uvy)
                )
                for rect in rects:
                    if rect.collidepoint((x2, y2)):
                        collisions.append((x2, y2))
            if len(collisions) > 0:
                bounce = (source, collision[0])
                for collision in collisions:
                    if distance(source, collision):
                        bounce = (source, collision)
                else:
                    bounce = None
            line_segments.append((source, bounce))
        if bounce:
            source = bounce
        else:
            bounce = None
    return line_segments
