import pygame
import os
from constants import *  # noqa:F403 flake8 ignore
'''
map builders
Linting is ignored in this file for "Line is too long"
'''


class Wall(pygame.sprite.Sprite):
    def __init__(self, center=None):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "wall.png"))
        self.rect = self.image.get_rect()
        if center:
            self.rect.centerx = center[0]
            self.rect.centery = center[1]

    # blit wall to screen
    def blit_sprite(self, surface):
        surface.blit(
            source=self.image,
            # adjust image by half of L x W to match rect
            dest=(self.rect.centerx - self.image.get_size()[0] // 2,
                  self.rect.centery - self.image.get_size()[1] // 2)
        )


# build walls by positioning according to the map
# maps are arrays of arrays
def array_to_walls(array):
    walls = []

    # y begins at 1 + width of the border + padding at the top + half wall size
    y = BORDER_WIDTH + TOP_PAD + WALL_SIZE // 2 + 1

    # for each row,
    for row in array:
        # x begins at 1 + wodth of the border + half wall size
        x = BORDER_WIDTH + WALL_SIZE // 2 + 1
        # for each column in the row
        for point in row:
            # build a wall if the column is truthy, and append it
            if point:
                walls.append(Wall((x, y)))

            # increment x by wall size
            x += WALL_SIZE

        # increment y by wall size
        y += WALL_SIZE

    # return a list of walls
    return walls


# build the borders of the map as a series of wall blocks
def build_borders(screen):
    borders = []

    # x begins at 0
    x = 0

    # from 0 to screen width
    while x < SCREEN_WIDTH:
        # append block at x, 0 and at x, SCREEN_HEIGHT
        borders.append(
            pygame.draw.rect(
                screen,
                WHITE,
                pygame.Rect(x, 0, BORDER_WIDTH, BORDER_WIDTH + TOP_PAD)
            ),
        )
        borders.append(
            pygame.draw.rect(
                screen,
                WHITE,
                pygame.Rect(x, SCREEN_HEIGHT - BORDER_WIDTH,
                            BORDER_WIDTH, BORDER_WIDTH)
            )
        )
        # increment x by borderwidth
        x += BORDER_WIDTH

    # from 0 to SCREEN HEIGHT
    y = TOP_PAD
    while y < SCREEN_HEIGHT:
        # append block at 0, y and at SCREEN WIDTH, y
        borders.append(
            pygame.draw.rect(
                screen,
                WHITE,
                pygame.Rect(0, y, BORDER_WIDTH, BORDER_WIDTH)
            )
        )
        borders.append(
            pygame.draw.rect(
                screen,
                WHITE,
                pygame.Rect(SCREEN_WIDTH - BORDER_WIDTH, y,
                            BORDER_WIDTH, BORDER_WIDTH)
            )
        )
        # increment y by BORDER WIDTH
        y += BORDER_WIDTH
    return borders


# create sprite.Group() with walls
def build_walls(map_walls):
    walls = pygame.sprite.Group()
    for wall in map_walls:
        walls.add(wall)
    return walls


# define a map
# walls should be truthy, space should be falsy
def testmap(X=1):
    '''
    Resolution
    25x18 blocks
    '''
    map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, X, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],

    ]

    # convert map to walls and return wall list
    return array_to_walls(map)


# define a map
# walls should be truthy, space should be falsy
def testmap2(X=1):
    '''
    Resolution
    25x18 blocks
    '''
    map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, X, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, X,],
        [0, 0, X, 0, 0, 0, 0, 0, X, X, X, X, 0, 0, X, 0, 0, 0, 0, X, 0, 0, 0, 0, X,],
        [0, 0, X, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, X, 0, 0, 0, 0, X,],
        [0, 0, X, 0, 0, 0, 0, 0, 0, 0, X, 0, 0, 0, X, 0, 0, 0, 0, X, 0, 0, 0, 0, X,],
        [0, 0, X, X, X, X, X, X, 0, 0, X, 0, 0, 0, 0, 0, 0, X, 0, X, 0, 0, 0, 0, X,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, X, 0, 0, 0, 0, 0, 0, X, 0, 0, 0, 0, 0, 0, X,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, X, 0, 0, 0, 0, 0, 0, 0,],
        [X, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, X,],
        [0, 0, X, 0, 0, 0, 0, 0, X, X, X, X, 0, 0, X, 0, 0, 0, 0, X, 0, 0, 0, 0, X,],
        [0, 0, X, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, X, 0, 0, 0, 0, X,],
        [0, 0, X, 0, 0, 0, 0, 0, 0, 0, X, 0, 0, 0, X, 0, 0, 0, 0, X, 0, 0, 0, 0, X,],
        [0, 0, X, X, X, X, X, X, 0, 0, X, 0, 0, 0, 0, 0, 0, X, 0, X, 0, 0, 0, 0, X,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, X, 0, 0, 0, 0, 0, 0, X, 0, 0, 0, 0, 0, 0, X,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, X, 0, 0, 0, 0, 0, 0, 0,],
        [X, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],

    ]

    # convert map to walls and return wall list
    return array_to_walls(map)
