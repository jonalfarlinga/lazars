from constants import *  # noqa=F403
import pygame
import os
from vector_math import calculate_line


class Player(pygame.sprite.Sprite):
    image = pygame.image.load(os.path.join("assets", "player.png"))
    # image = pygame.image.load(os.path.join("assets", "tank.png"))
    # image.set_colorkey(BLACK)
    # pygame.transform.rotate(image, -135)
    rect = image.get_rect()
    rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    direction = 45  # player facing in degrees
    bounces = 5
    speed = 5

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
                    self.rect.centery += self.speed + 1
            self.rect.centery -= self.speed
        if keys[pygame.K_s]:
            for i in rect_cols:
                if rects[i].centery > self.rect.centery:
                    self.rect.centery -= self.speed + 1
            self.rect.centery += self.speed
        if keys[pygame.K_a]:
            for i in rect_cols:
                if rects[i].centerx < self.rect.centerx:
                    self.rect.centerx += self.speed + 1
            self.rect.centerx -= self.speed
        if keys[pygame.K_d]:
            for i in rect_cols:
                if rects[i].centerx > self.rect.centerx:
                    self.rect.centerx -= self.speed + 1
            self.rect.centerx += self.speed

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
                BLACK,
                origin,
                point,
                width=3,
            )
            origin = point
