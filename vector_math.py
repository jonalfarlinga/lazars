import math
from constants import *  # noqa:F403 flake8 ignore


# converts a heading to a unit vector
def deg_to_vector(deg):
    unit_vector = (
        math.cos((deg * math.pi) / 180),
        math.sin((deg * math.pi) / 180)
    )
    return unit_vector


# radian to vector
def rad_to_vector(rad):
    unit_vector = (
        math.cos(rad),
        math.sin(rad)
    )
    return unit_vector


# measures and returns the distance between two coordinates
def distance(point1, point2):
    distance = math.sqrt(
        (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2
    )
    return distance


# takes a point and radian direction and an new coord component,
# if terms_of_x returns y2
# else returns x2
def param_eq(source, new, rad, terms_of_x=True):
    x1, y1 = source
    if terms_of_x:
        return y1 + ((new - x1) * math.sin(rad) / math.cos(rad))
    else:
        return x1 + ((new - y1) * math.cos(rad) / math.sin(rad))


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
def proper_round(num):
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


'''
# given a point, bearing and list of rects
# finds the line and 4 reflections, and returns a list of point pairs.
def calculate_line(source, deg, rects, bounces):
    bounce_points = []
    uvx, uvy = deg_to_vector(deg)
    while source and len(bounce_points) < bounces:
        bounce = None
        if uvx > .7071 and (-.7072 <= uvy <= .7072):
            # start = source
            # for range(start, SCREEN, 20)
            #     if collide:
            #         continue (start = start, end = current range)
            # else:
            #     start = current range
            start = source
            vector_dif = round(uvy / uvx, 5)
            for runx in range(start[0] + 1, SCREEN_WIDTH + 20, 20):
                for rect in rects:
                    runy = proper_round(
                        start[1] + (runx - start[0]) * vector_dif
                    )
                    if rect.collidepoint((runx, runy)):
                        for x2 in range(start[0] + 1, runx + 1):
                            y2 = proper_round(
                                runy + (x2 - runx) * vector_dif
                            )
                            if rect.collidepoint((x2, y2)):
                                bounce = ((x2, y2))
                                uvx, uvy = reflect_direction(uvx, uvy, x2 - 1,
                                                             rect, True)
                                break
                    if bounce:
                        break
                if bounce:
                    break
                start = runx, runy
        elif uvx <= -.7071 and (-.7072 <= uvy <= .7072):
            start = source
            vector_dif = round(uvy / uvx, 5)
            for runx in reversed(range(0, start[0] - 1, 20)):
                for rect in rects:
                    runy = proper_round(
                        start[1] + (runx - start[0]) * vector_dif
                    )
                    if rect.collidepoint((runx, runy)):
                        for x2 in reversed(range(runx - 1, start[0])):
                            y2 = proper_round(
                                runy + (runx - runx) * vector_dif
                            )
                            if rect.collidepoint((x2, y2)):
                                bounce = ((x2, y2))
                                uvx, uvy = reflect_direction(uvx, uvy, x2 + 1,
                                                             rect, True)
                                break
                    if bounce:
                        break
                if bounce:
                    break
                start = runx, runy
        elif uvy > .7071 and (-.7072 <= uvx <= .7072):
            start = source
            vector_dif = round(uvx / uvy, 5)
            for runy in range(start[1] + 1, SCREEN_HEIGHT + 20, 20):
                for rect in rects:
                    runx = proper_round(
                        start[0] + (runy - start[1]) * vector_dif
                    )
                    if rect.collidepoint((runx, runy)):
                        for y2 in range(start[1] + 1, runy + 1):
                            x2 = proper_round(
                                runx + (y2 - runy) * vector_dif
                            )
                            if rect.collidepoint((x2, y2)):
                                bounce = ((x2, y2))
                                uvx, uvy = reflect_direction(uvx, uvy, y2 - 1,
                                                             rect, False)
                                break
                    if bounce:
                        break
                if bounce:
                    break
        elif uvy <= -.7071 and (-.7072 <= uvx <= .7072):
            start = source
            vector_dif = round(uvx / uvy, 5)
            for runy in reversed(range(0, start[1] - 1, 20)):
                for rect in rects:
                    runx = proper_round(
                        start[0] + (runy - start[1]) * vector_dif
                    )
                    if rect.collidepoint((runx, runy)):
                        for y2 in reversed(range(runy, start[1])):
                            x2 = proper_round(
                                runx + (y2 - runy) * vector_dif
                            )
                            if rect.collidepoint((x2, y2)):
                                bounce = ((x2, y2))
                                uvx, uvy = reflect_direction(uvx, uvy, y2 + 1,
                                                             rect, False)
                                break
                    if bounce:
                        break
                if bounce:
                    break
        if bounce:
            bounce_points.append(bounce)
            source = bounce
        else:
            source = None
    return bounce_points
'''


# given a point, bearing and list of rects
# finds the line and 4 reflections, and returns a list of point pairs.
def calculate_line(source, rad, rects, bounces):
    # while source and bounces less than bounces
    #   draw a line from source to SCREEN_EDGE <-- SCREEN_EDGE is based on quad
    #       find all collisions with rects
    # noqa      find rect according to rect.edge closest to player <-- closest edge based on quadrant
    # noqa          calculate x2 or y2 by player angle and rect.edge <-- linear eq based on quadrant
    # noqa          --> linear_eq(source, rect.edge, rad_to_vector(rad))
    #               assign bounce
    #               reflect off of rect
    #               --> uvx, uvy = reflect_direction(uvx, uvy, y2 + 1,
    #                                                        rect, False)
    #   append bounce
    #   source = bounce
    pass
