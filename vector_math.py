import math
from constants import *  # noqa:F403 flake8 ignore


# converts a bearing to a unit vector
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
# if last is an x coordinate, term_of_x should be true
# if last is a y coordinate, terms_of_x should be false
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
def calculate_line(source, deg, rects, bounces):
    bounce_points = []
    uvx, uvy = deg_to_vector(deg)
    while source and len(bounce_points) < bounces:
        bounce = None
        if abs(uvx) > abs(uvy):
            for x in range(source[0], SCREEN_WIDTH + 1, 20):
                for rect in rects:
                    y = round(source[1] + (x - source[0]) * uvy / uvx)
                    if rect.collidepoint((x, y)):
                        bounce = ((x, y))
                        uvx, uvy = reflect_direction(uvx, uvy, x, rect, True)
                        break
                if bounce:
                    break
        else:
            for y in range(source[1], SCREEN_HEIGHT + 1, 20):
                for rect in rects:
                    x = round(source[0] + (y - source[1]) * uvx / uvy)
                    if rect.collidepoint((x, y)):
                        bounce = ((x, y))
                        uvx, uvy = reflect_direction(uvx, uvy, y, rect, False)
                        break
                if bounce:
                    break
        if bounce:
            bounce_points.append(bounce)
            source = bounce
        else:
            source = None
    return bounce_points


# def calculate_line(source, deg, rects, bounces):
#     bounce_points = []
#     uvx, uvy = deg_to_vector(deg)
#     while source and len(bounce_points) < bounces:
#         bounce = None
#         if uvx > .7071 and (-.7072 <= uvy <= .7072):
#             # start = source
#             # for range(start, SCREEN, 20)
#             #     if collide:
#             #         continue (start = start, end = current range)
#             # else:
#             #     start = current range
#             start = source
#             vector_dif = round(uvy / uvx, 5)
#             for runx in range(start[0] + 1, SCREEN_WIDTH + 20, 20):
#                 for rect in rects:
#                     runy = proper_round(
#                         start[1] + (runx - start[0]) * vector_dif
#                     )
#                     if rect.collidepoint((runx, runy)):
#                         for x2 in range(start[0] + 1, runx + 1):
#                             y2 = proper_round(
#                                 runy + (x2 - runx) * vector_dif
#                             )
#                             if rect.collidepoint((x2, y2)):
#                                 bounce = ((x2, y2))
#                                 uvx, uvy = reflect_direction(uvx, uvy, x2 - 1,
#                                                              rect, True)
#                                 break
#                     if bounce:
#                         break
#                 if bounce:
#                     break
#                 start = runx, runy
#         elif uvx <= -.7071 and (-.7072 <= uvy <= .7072):
#             start = source
#             vector_dif = round(uvy / uvx, 5)
#             for runx in reversed(range(0, start[0] - 1, 20)):
#                 for rect in rects:
#                     runy = proper_round(
#                         start[1] + (runx - start[0]) * vector_dif
#                     )
#                     if rect.collidepoint((runx, runy)):
#                         for x2 in reversed(range(runx - 1, start[0])):
#                             y2 = proper_round(
#                                 runy + (runx - runx) * vector_dif
#                             )
#                             if rect.collidepoint((x2, y2)):
#                                 bounce = ((x2, y2))
#                                 uvx, uvy = reflect_direction(uvx, uvy, x2 + 1,
#                                                              rect, True)
#                                 break
#                     if bounce:
#                         break
#                 if bounce:
#                     break
#                 start = runx, runy
#         elif uvy > .7071 and (-.7072 <= uvx <= .7072):
#             start = source
#             vector_dif = round(uvx / uvy, 5)
#             for runy in range(start[1] + 1, SCREEN_HEIGHT + 20, 20):
#                 for rect in rects:
#                     runx = proper_round(
#                         start[0] + (runy - start[1]) * vector_dif
#                     )
#                     if rect.collidepoint((runx, runy)):
#                         for y2 in range(start[1] + 1, runy + 1):
#                             x2 = proper_round(
#                                 runx + (y2 - runy) * vector_dif
#                             )
#                             if rect.collidepoint((x2, y2)):
#                                 bounce = ((x2, y2))
#                                 uvx, uvy = reflect_direction(uvx, uvy, y2 - 1,
#                                                              rect, False)
#                                 break
#                     if bounce:
#                         break
#                 if bounce:
#                     break
#         elif uvy <= -.7071 and (-.7072 <= uvx <= .7072):
#             start = source
#             vector_dif = round(uvx / uvy, 5)
#             for runy in reversed(range(0, start[1] - 1, 20)):
#                 for rect in rects:
#                     runx = proper_round(
#                         start[0] + (runy - start[1]) * vector_dif
#                     )
#                     if rect.collidepoint((runx, runy)):
#                         for y2 in reversed(range(runy, start[1])):
#                             x2 = proper_round(
#                                 runx + (y2 - runy) * vector_dif
#                             )
#                             if rect.collidepoint((x2, y2)):
#                                 bounce = ((x2, y2))
#                                 uvx, uvy = reflect_direction(uvx, uvy, y2 + 1,
#                                                              rect, False)
#                                 break
#                     if bounce:
#                         break
#                 if bounce:
#                     break
#         if bounce:
#             bounce_points.append(bounce)
#             source = bounce
#         else:
#             source = None
#     return bounce_points

'''
# assumes all collision rects are square.
def find_bounce(source, rad, rects, ray):
    if rad < PI:
        refrad = rad + PI
    else:
        refrad = rad - PI
    collide_list = ray.collidelistall(rects)
    if PI * 1.25 < refrad <= PI * 1.75:  # 5pi/4 to 7pi/4
        stop = 0
        for index in collide_list:
            rect = rects[index]
            if rect.bottom > stop:
                stop = rect.bottom
        y2 = stop
        x2 = source[1] + (
            (stop - source[0]) * math.cos(rad) / math.sin(rad)
        )
        if rad < PI:
            rad = PI2 + PI - rad
        else:
            rad = PI2 + PI - rad
    elif PI * .75 < refrad <= PI * 1.25:  # 3pi/4 to 5pi/4
        stop = SCREEN_WIDTH
        for index in collide_list:
            rect = rects[index]
            if rect.left < stop:
                stop = rect.left
        x2 = stop
        y2 = source[1] + (
            (stop - source[0]) * math.sin(rad) / math.cos(rad)
        )
        if rad < PI:
            rad = PI2 + PI - rad
        else:
            rad = PI2 + PI - rad
    elif PI / 4 < refrad <= PI * .75:  # pi/4 to 3pi/4
        stop = SCREEN_HEIGHT
        for index in collide_list:
            rect = rects[index]
            if rect.top < stop:
                stop = rect.top
        y2 = stop
        x2 = source[0] + (
            (stop - source[1]) * math.cos(rad) / math.sin(rad)
        )
        if rad < PI:
            rad = PI2 + PI - rad
        else:
            rad = PI2 + PI - rad
    else:   # remaimder is < pi/4 or > 7pi/4
        stop = 0
        for index in collide_list:
            rect = rects[index]
            if rect.right > stop:
                stop = rect.right
        x2 = stop
        y2 = source[1] + (
            (stop - source[0]) * math.sin(rad) / math.cos(rad)
        )
        if rad < PI:
            rad = PI2 + PI - rad
        else:
            rad = PI2 + PI - rad
    return x2, y2, rad


# given a point, bearing and list of rects
# finds the line and 4 reflections, and returns a list of point pairs.
def calculate_line(source, deg, rects, bounces):
    bounce_points = []

    # convert degrees to a unit vector pair
    uvx, uvy = deg_to_vector(deg)

    # while a valid source exists, and len((bounces) less than player.bounces
    while source and len(bounce_points) < bounces:
        if PI / 4 < rad <= PI * .75:       # pi/4 to 3pi/4
            wally = SCREEN_HEIGHT
            wallx = source[0] + (
                (SCREEN_HEIGHT - source[1]) * math.cos(rad) / math.sin(rad)
            )
        elif PI * .75 < rad <= PI * 1.25:  # 3pi/4 to 5pi/4
            wallx = 0
            wally = source[1] + (
                (0 - source[0]) * math.sin(rad) / math.cos(rad)
            )
        elif PI * 1.25 < rad <= PI * 1.75:  # 5pi//4 to 7pi/4
            wally = 0
            wallx = source[0] + (
                (0 - source[1]) * math.cos(rad) / math.sin(rad)
            )
        else:   # remainder is < p/4 or > 7pi/4
            wallx = SCREEN_WIDTH
            wally = source[1] + (
                (SCREEN_WIDTH - source[0]) * math.sin(rad) / math.cos(rad)
            )
        ray = line(
            screen,
            NONE_COLOR,
            source,
            (wallx, wally),
        )
        x2, y2, rad = find_bounce(source, rad, rects, ray)
        bounce_points.append((x2, y2))
        source = (x2, y2)
        # reset bounce
        bounce = None
        if uvx > .7071 and (-.7072 <= uvy <= .7072):  # deg < 45 or > 315

            # calculate the vector portion of the linear equation once
            # to save on processing time
            vector_dif = round(uvy / uvx, 5)

            # check of blocks along vector every 20 pixels from player to
            # SCREEN_WIDTH. This is a critical error in the program, but it
            # speeds up processing. Correcting this error prompted restarting
            # the project.
            for runx in range(source[0] + 1, SCREEN_WIDTH + 20, 20):
                # find runy using source, runx, and vector_dif
                runy = proper_round(
                    source[1] + (runx - source[0]) * vector_dif
                )
                for rect in rects:
                    # for each rect, check if it collides with runx, runy
                    if rect.collidepoint((runx, runy)):
                        # if collision, check pixel-pixel for first collision
                        for x2 in range(source[0] + 1, runx + 1):
                            y2 = proper_round(
                                runy + (x2 - runx) * vector_dif
                            )
                            if rect.collidepoint((x2, y2)):
                                # with first collision,
                                # create bounce using x2, y2
                                bounce = (x2, y2)
                                # find the reflected uvx/uvy
                                uvx, uvy = reflect_direction(uvx, uvy, x2 - 1,
                                                             rect, True)
                                # after we have a bounce, break
                                break
                    # cancel the search if we found a bounce
                    if bounce:
                        break
                # cancel the search if we found a bounce
                if bounce:
                    break
        elif uvx <= -.7071 and (-.7072 <= uvy <= .7072):  # 135 < deg < 225
            # repeated pattern. see comments under "if" statement
            vector_dif = round(uvy / uvx, 5)
            for runx in reversed(range(0, source[0] - 1, 20)):
                runy = proper_round(
                    source[1] + (runx - source[0]) * vector_dif
                )
                for rect in rects:
                    if rect.collidepoint((runx, runy)):
                        for x2 in reversed(range(runx - 1, source[0])):
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
        elif uvy > .7071 and (-.7072 <= uvx <= .7072):  # 225 < deg < 315
            # repeated pattern. See comment under "if" statement
            vector_dif = round(uvx / uvy, 5)
            for runy in range(source[1] + 1, SCREEN_HEIGHT + 20, 20):
                runx = proper_round(
                    source[0] + (runy - source[1]) * vector_dif
                )
                for rect in rects:
                    if rect.collidepoint((runx, runy)):
                        for y2 in range(source[1] + 1, runy + 1):
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
        elif uvy <= -.7071 and (-.7072 <= uvx <= .7072):  # 45 < deg < 135
            # repeated pattern. See comments under "if" statement
            vector_dif = round(uvx / uvy, 5)
            for runy in reversed(range(0, source[1] - 1, 20)):
                runx = proper_round(
                    source[0] + (runy - source[1]) * vector_dif
                )
                for rect in rects:
                    if rect.collidepoint((runx, runy)):
                        for y2 in reversed(range(runy, source[1])):
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
        # if a bounce was found, add it to bounce_points and change source
        if bounce:
            bounce_points.append(bounce)
            source = bounce
        # else, source is invalid, breaking the loop.
        else:
            source = None
    return bounce_points
'''
