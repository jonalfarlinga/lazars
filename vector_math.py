import math
from constants import *  # noqa:F403 flake8 ignore


# converts a heading to a unit vector
def deg_to_vector(deg):
    unit_vector = (
        math.cos((deg * math.pi) / 180),
        math.sin((deg * math.pi) / 180)
    )
    return unit_vector


# measures and returns the distance between two coordinates
def distance(point1, point2):
    distance = math.sqrt(
        (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2
    )
    return distance


# takes a point and vector and an x2, returns y2
def linear_eq(source, x2, unit_vector):
    x1, y1 = source
    uvx, uvy = unit_vector
    return y1 + ((x2 - x1) / uvx * uvy)


# takes a point and vector and a y2, returns x2
def linear_eq_inv(source, y2, unit_vector):
    x1, y1 = source
    uvx, uvy = unit_vector
    return x1 + ((y2 - y1) / uvy * uvx)


# rounds up for decimals 0.5 and above, or rounds down
def round(num):
    test = num * 10
    if test % 10 >= 5:
        return math.ceil(num)
    else:
        return math.floor(num)


# takes x/y vector components, the previous key value, and a rect
# returns a reflected vector
def reflect_direction(uvx, uvy, last, rect, terms_of_x):
    if terms_of_x:
        if rect.left < last < rect.right:
            uvy = -uvy
        else:
            uvx = -uvx
    else:
        if rect.top < last < rect.bottom:
            uvx = -uvx
        else:
            uvy = -uvy
    return uvx, uvy


# given a point, bearing and list of rects
# finds the line and 4 reflections, and returns a list of point pairs.
def calculate_line(source, deg, rects):
    bounce_points = []
    uvx, uvy = deg_to_vector(deg)
    while source and len(bounce_points) < BOUNCES:
        bounce = None
        if uvx > .7071 and (-.7072 <= uvy <= .7072):
            for x2 in range(source[0] + 1, SCREEN_WIDTH):
                y2 = round(
                    linear_eq(source, x2, (uvx, uvy))
                )
                for rect in rects:
                    if rect.collidepoint((x2, y2)):
                        bounce = ((x2, y2))
                        break
                if bounce:
                    uvx, uvy = reflect_direction(uvx, uvy, x2 - 1, rect, True)
                    break
        elif uvx <= -.7071 and (-.7072 <= uvy <= .7072):
            for x2 in reversed(range(0, source[0] - 1)):
                y2 = round(
                    linear_eq(source, x2, (uvx, uvy))
                )
                for rect in rects:
                    if rect.collidepoint((x2, y2)):
                        bounce = ((x2, y2))
                        break
                if bounce:
                    uvx, uvy = reflect_direction(uvx, uvy, x2 + 1, rect, True)
                    break
        elif uvy > .7071 and (-.7072 <= uvx <= .7072):
            for y2 in range(source[1] + 1, SCREEN_HEIGHT):
                x2 = round(
                    linear_eq_inv(source, y2, (uvx, uvy))
                )
                for rect in rects:
                    if rect.collidepoint((x2, y2)):
                        bounce = ((x2, y2))
                        break
                if bounce:
                    uvx, uvy = reflect_direction(uvx, uvy, y2 - 1, rect, False)
                    break
        elif uvy <= -.7071 and (-.7072 <= uvx <= .7072):
            for y2 in reversed(range(0, source[1] - 1)):
                x2 = round(
                    linear_eq_inv(source, y2, (uvx, uvy))
                )
                for rect in rects:
                    if rect.collidepoint((x2, y2)):
                        bounce = ((x2, y2))
                        break
                if bounce:
                    uvx, uvy = reflect_direction(uvx, uvy, y2 + 1, rect, False)
                    break
        bounce_points.append(bounce)
        source = bounce
    return bounce_points
