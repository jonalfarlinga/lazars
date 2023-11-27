import pygame
import sys
import os
# from debug_me import debug
import maps
from constants import *  # noqa:F403
from vector_math import calculate_line


'''
set up constants
'''
# initialize the pygame module
pygame.init()

# load and set the logo
logo = pygame.image.load(os.path.join("assets", "laser.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Lazars")
font = pygame.font.SysFont("Arial", 20)


'''
create classes
'''


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.direction = 45  # player facing in degrees

    def blit_sprite(self, surface):
        surface.blit(
            source=self.image,
            dest=(self.rect.centerx - self.image.get_size()[0] // 2,
                  self.rect.centery - self.image.get_size()[1] // 2)
        )

    def move(self, rects):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction -= 1
            print(self.direction)
            if self.direction < 0:
                self.direction = 359
        elif keys[pygame.K_RIGHT]:
            self.direction += 1
            print(self.direction)
            if self.direction > 359:
                self.direction = 0
        rect_cols = self.rect.collidelistall(rects)
        if keys[pygame.K_w]:
            for i in rect_cols:
                if rects[i].centery < self.rect.centery:
                    self.rect.centery += 2
            self.rect.centery -= 1
        if keys[pygame.K_s]:
            for i in rect_cols:
                if rects[i].centery > self.rect.centery:
                    self.rect.centery -= 2
            self.rect.centery += 1
        if keys[pygame.K_a]:
            for i in rect_cols:
                if rects[i].centerx < self.rect.centerx:
                    self.rect.centerx += 2
            self.rect.centerx -= 1
        if keys[pygame.K_d]:
            for i in rect_cols:
                if rects[i].centerx > self.rect.centerx:
                    self.rect.centerx -= 2
            self.rect.centerx += 1

    def laser(self, screen, rects):
        line_segments = calculate_line(self.rect.center, self.direction, rects)
        for segment in line_segments:
            if segment[1] is None:
                segment = (segment[0], (0, 0))
            pygame.draw.line(
                screen,
                BLACK,
                segment[0],
                segment[1],
                width=3,
            )


def print_background(screen):
    screen.fill(WHITE)
    pygame.draw.lines(
        screen,
        RED,
        True,
        [
            (0, TOP_PAD),
            (0, SCREEN_HEIGHT),
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            (SCREEN_WIDTH, TOP_PAD)
        ],
        BORDER_WIDTH * 2
    )


'''
initialize game environment
'''
# create a surface on screen and initialize entities
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
borders = maps.build_borders(screen)

walls = pygame.sprite.Group()
for wall in maps.testmap():
    walls.add(wall)

player = Player()
player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

FramesPerSecond = pygame.time.Clock()


# define a main function
def main():
    pygame.display.flip()

    # main loop
    while True:
        print_background(screen)
        rects = []
        for block in borders + walls.sprites():
            if hasattr(block, "blit_sprite"):
                block.blit_sprite(screen)
            if hasattr(block, "rect"):
                rects.append(block.rect)
            else:
                rects.append(block)

        # debug(pygame.mouse.get_pos(), screen, rects)  # debug functions
        player.move(rects)
        player.blit_sprite(screen)
        player.laser(screen, rects)
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                pygame.quit()
                sys.exit()
        pygame.time.delay(1)
        FramesPerSecond.tick(FPS)
        pygame.display.update()


# run the main function only if this module is executed as the main script
if __name__ == "__main__":
    main()
