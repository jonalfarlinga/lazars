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


def reflect_direction(uvx, uvy, source, bounce, rects):
    reflect = -uvx, uvy
    if source[0] < bounce[0]:
        test_point = (bounce[0]+1, round(linear_eq(bounce, bounce[0]+1, reflect)))
        collision = False
        for rect in rects:
            if rect.collidepoint(test_point):
                collision = True
        if collision:
            uvy = -uvy
        else:
            uvx = -uvx
    else:
        test_point = (bounce[0]-1, round(linear_eq(bounce, bounce[0]-1, reflect)))
        collision = False
        for rect in rects:
            if rect.collidepoint(test_point):
                collision = True
        if collision:
            uvy = -uvy
        else:
            uvx = -uvx
    return uvx, uvy


def calculate_line(source, deg, rects):
    line_segments = []
    uvx, uvy = deg_to_vector(deg)
    while source and len(line_segments) < 5:
        bounce = None
        # check forward for x if
        if uvx > .7071 and (-.7072 <= uvy <= .7072):
            for x2 in range(source[0]+1, SCREEN_WIDTH):
                y2 = round(
                    linear_eq(source, x2, (uvx, uvy))
                )
                for rect in rects:
                    if rect.collidepoint((x2, y2)):
                        bounce = ((x2, y2))
                        break
                if bounce:
                    uvx, uvy = reflect_direction(uvx, uvy, source, bounce, rects)
                    break
        elif uvx <= -.7071 and (-.7072 <= uvy <= .7072):
            for x2 in reversed(range(0, source[0]-1)):
                y2 = round(
                    linear_eq(source, x2, (uvx, uvy))
                )
                for rect in rects:
                    if rect.collidepoint((x2, y2)):
                        bounce = ((x2, y2))
                        break
                if bounce:
                    uvx, uvy = reflect_direction(uvx, uvy, source, bounce, rects)
                    break
        elif uvy > .7071 and (-.7072 <= uvx <= .7072):
            for y2 in range(source[1]+1, SCREEN_HEIGHT):
                x2 = round(
                    linear_eq_inv(source, y2, (uvx, uvy))
                )
                for rect in rects:
                    if rect.collidepoint((x2, y2)):
                        bounce = ((x2, y2))
                        break
                if bounce:
                    break
        elif uvy <= -.7071 and (-.7072 <= uvx <= .7072):
            for y2 in reversed(range(0, source[1]-1)):
                x2 = round(
                    linear_eq_inv(source, y2, (uvx, uvy))
                )
                for rect in rects:
                    if rect.collidepoint((x2, y2)):
                        bounce = ((x2, y2))
                        break
                if bounce:
                    break
        line_segments.append((source, bounce))
        source = bounce
    return line_segments
