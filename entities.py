from constants import *  # noqa=F403
import pygame
import os
from vector_math import calculate_line


class Player(pygame.sprite.Sprite):
    # image = pygame.image.load(os.path.join("assets", "player.png"))
    direction = 45  # player facing in degrees
    bounces = 5
    speed = 5
    img_source = os.path.join("assets", "tank.png")
    image = pygame.image.load(img_source)
    image.set_colorkey(BLACK)
    image = pygame.transform.rotate(image, direction - 180)
    rect = image.get_rect()
    rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def blit_sprite(self, surface):
        surface.blit(
            source=self.image,
            dest=(self.rect.centerx - self.image.get_size()[0] // 2,
                  self.rect.centery - self.image.get_size()[1] // 2)
        )

    def move(self, rects):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction -= 2.5
            self.image = pygame.transform.rotate(
                pygame.image.load(self.img_source),
                -90 - self.direction,
            )
            self.image.set_colorkey(BLACK)
            if self.direction < 0:
                self.direction = self.direction + 360
            print(self.direction)
        elif keys[pygame.K_RIGHT]:
            self.direction += 2.5
            self.image = pygame.transform.rotate(
                pygame.image.load(self.img_source),
                -90 - self.direction,
            )
            self.image.set_colorkey(BLACK)
            if self.direction > 359:
                self.direction = 0
            print(self.direction)
        rect_cols = self.rect.collidelistall(rects)
        if keys[pygame.K_w]:
            for px in range(self.speed):
                stop = False
                for i in rect_cols:
                    above = all(
                        [
                            rects[i].bottom >= self.rect.top,
                            rects[i].centery <= self.rect.centery,
                            rects[i].left <= self.rect.centerx,
                            rects[i].right >= self.rect.centerx,
                        ]
                    )
                    if above:
                        stop = True
                        self.rect.centery += 1
                        break
                self.rect.centery -= 1
        if keys[pygame.K_s]:
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
        if keys[pygame.K_a]:
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
        if keys[pygame.K_d]:
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

    def laser(self, screen, rects):
        line_segments = calculate_line(
            self.rect.center,
            self.direction,
            rects,
            self.bounces)
        origin = self.rect.center
        for point in line_segments:
            pygame.draw.line(
                screen,
                LASER,
                origin,
                point,
                width=3,
            )
            origin = point
