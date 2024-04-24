from .constants import *  # noqa=F403
import pygame
import os
from .vector_math import calculate_line


class Player(pygame.sprite.Sprite):
    direction = 0  # player facing in degrees
    bounces = 5
    speed = 5

    # set player image
    img_source = os.path.join("assets", "tank.png")
    image = pygame.image.load(img_source)
    image.set_colorkey(BLACK)
    image = pygame.transform.rotate(image, direction - 180)

    # set player rect
    rect = image.get_rect()
    rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # blit player image to screen
    def blit_sprite(self, surface):
        surface.blit(
            source=self.image,
            # offset by half L x W to match rect
            dest=(self.rect.centerx - self.image.get_size()[0] // 2,
                  self.rect.centery - self.image.get_size()[1] // 2)
        )

    # check player input and process movement actions
    def move(self, rects):
        # get the activated keys
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:         # <- key:
            # reduce player angle
            self.direction -= 2.5
            # reset player image angle
            self.image = pygame.transform.rotate(
                pygame.image.load(self.img_source),
                # adjust to match player direction with pygame direction
                -90 - self.direction,
            )
            self.image.set_colorkey(BLACK)

            # keep player angle in 0-360
            if self.direction < 0:
                self.direction += 360
            print(self.direction)  # for debugging
        elif keys[pygame.K_RIGHT]:       # -> key
            # increase player angle
            self.direction += 2.5
            # reset player image angle
            self.image = pygame.transform.rotate(
                pygame.image.load(self.img_source),
                -90 - self.direction,
            )
            self.image.set_colorkey(BLACK)

            # keep player angle in 0-360
            if self.direction > 359:
                self.direction -= 360
            print(self.direction)  # for debugging

        # find collisions
        rect_cols = self.rect.collidelistall(rects)

        if keys[pygame.K_w]:            # W key
            # step through speed one px at a time
            for px in range(self.speed):
                # stop = True if the player encounters a wall
                stop = False

                # each step, check all collisions
                for i in rect_cols:
                    # boolean for collided rect is above the player, player
                    # center is between left and right
                    above = all(
                        [
                            rects[i].bottom >= self.rect.top,
                            rects[i].centery <= self.rect.centery,
                            rects[i].left <= self.rect.centerx,
                            rects[i].right >= self.rect.centerx,
                        ]
                    )
                    if above:
                        # if coliided block is above, stop the player
                        stop = True
                        break
                # if the player is not stopped, decrement centery
                if not stop:
                    self.rect.centery -= 1

        if keys[pygame.K_s]:            # S key
            # repeats pattern from above. See W key comments
            for px in range(self.speed):
                stop = False
                for i in rect_cols:
                    below = all(
                        [
                            rects[i].top <= self.rect.bottom,
                            rects[i].centery >= self.rect.centery,
                            rects[i].left <= self.rect.centerx,
                            rects[i].right >= self.rect.centerx,
                        ]
                    )
                    if below:
                        stop = True
                        break
                if not stop:
                    self.rect.centery += 1
        if keys[pygame.K_a]:            # A key
            # repeats pattern from above. See W key comments
            for px in range(self.speed):
                stop = False
                for i in rect_cols:
                    left = all(
                        [
                            rects[i].right >= self.rect.left,
                            rects[i].centerx <= self.rect.centerx,
                            rects[i].top <= self.rect.centery,
                            rects[i].bottom >= self.rect.centery,
                        ]
                    )
                    if left:
                        stop = True
                        break
                if not stop:
                    self.rect.centerx -= 1
        if keys[pygame.K_d]:            # D key
            # repeats pattern from above. See W key comments
            for px in range(self.speed):
                stop = False
                for i in rect_cols:
                    right = all(
                        [
                            rects[i].left <= self.rect.right,
                            rects[i].centerx >= self.rect.centerx,
                            rects[i].top <= self.rect.centery,
                            rects[i].bottom >= self.rect.centery
                        ]
                    )
                    if right:
                        stop = True
                        break
                if not stop:
                    self.rect.centerx += 1

    # find laser bounces and blit lines
    def laser(self, screen, rects):
        # calculate bounce pints
        bounce_points = calculate_line(
            self.rect.center,
            self.direction,
            rects,
            self.bounces)

        # origin starts at player position
        origin = self.rect.center

        # for each bounce point
        for point in bounce_points:
            # draw a line from origin to bounce
            pygame.draw.aaline(
                screen,
                LASER,
                origin,
                point,
                # width=3,
            )
            # set new origin at previous bounce
            origin = point
