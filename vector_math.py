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


def calculate_line(source, deg, rects):
    line_segments = []
    while len(line_segments) < 3:
        bounce = None
        x1, y1 = source
        uvx, uvy = deg_to_vector(deg)
        if uvx > 0:
            for x2 in range(x1+1, SCREEN_WIDTH):
                collisions = []
                x2 = x1 + 1
                y2 = {
                    y1 + ((x2 - x1) / uvx) * uvy
                }
                for rect in rects:
                    if rect.collidepoint(x2, y2):
                        collisions.append((x2, y2))
            bounce = (source, collision[0])
            for collision in collisions:
                if distance(source, collision):
                    bounce = (source, collision)
            line_segments.append((source, bounce))
        if bounce:
            source = bounce
        else:
            break
    return line_segments
