"""Enemy entities — patrol and sentry types."""

import math
import random
import pygame

from src.bullet import Bullet
from assets.sprites import make_enemy_patrol_sprite, make_enemy_sentry_sprite


class PatrolEnemy:
    """Patrolling enemy that walks back and forth on a platform."""

    def __init__(self, x, y, patrol_range, speed=1.5):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 36
        self.hp = 1
        self.alive = True
        self.speed = speed
        self.facing = -1  # starts facing left
        self.patrol_min, self.patrol_max = patrol_range
        self.vy = 0
        self.on_ground = False
        self.sprite = make_enemy_patrol_sprite(2)
        self.death_timer = 0

    @property
    def rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y - self.height,
                           self.width, self.height)

    def update(self, terrain_rects):
        if not self.alive:
            self.death_timer -= 1
            return self.death_timer <= 0  # remove when timer expires

        # Move
        self.x += self.speed * self.facing

        # Patrol bounds
        if self.x <= self.patrol_min:
            self.x = self.patrol_min
            self.facing = 1
        elif self.x >= self.patrol_max:
            self.x = self.patrol_max
            self.facing = -1

        # Gravity
        self.vy += 0.5
        self.y += self.vy
        self.on_ground = False
        for rect in terrain_rects:
            if self.rect.colliderect(rect):
                if self.vy > 0:
                    self.y = rect.top
                    self.vy = 0
                    self.on_ground = True

        return False

    def take_damage(self):
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            self.death_timer = 15
            return True
        return False

    def draw(self, surf, camera_x):
        sx = int(self.x - camera_x)
        sy = int(self.y)
        if not self.alive:
            if self.death_timer % 3 == 0:
                pygame.draw.circle(surf, (255, 200, 50), (sx, sy - 18), 12)
                pygame.draw.circle(surf, (255, 100, 0), (sx, sy - 18), 8)
            return
        draw = pygame.transform.flip(self.sprite, self.facing == 1, False)
        surf.blit(draw, (sx - 18, sy - 24))


class SentryEnemy:
    """Stationary enemy that shoots at the player."""

    def __init__(self, x, y, shoot_interval=1.5):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 24
        self.hp = 1
        self.alive = True
        self.shoot_interval = shoot_interval
        self.shoot_timer = 0
        self.facing = -1
        self.sprite = make_enemy_sentry_sprite(2)
        self.death_timer = 0

    @property
    def rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y - self.height,
                           self.width, self.height)

    def update(self, terrain_rects, player_x, player_y, dt):
        if not self.alive:
            self.death_timer -= 1
            return False, None

        # Face player
        self.facing = 1 if player_x > self.x else -1

        # Shooting timer
        self.shoot_timer -= dt
        bullet = None
        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_interval
            # Aim at player
            dx = player_x - self.x
            dy = player_y - self.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 0:
                angle = math.degrees(math.atan2(-dy, dx))
                bullet = Bullet(self.x, self.y - 10, angle, 5,
                                owner='enemy', weapon_type='BASIC')

        return False, bullet

    def take_damage(self):
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            self.death_timer = 15
            return True
        return False

    def draw(self, surf, camera_x):
        sx = int(self.x - camera_x)
        sy = int(self.y)
        if not self.alive:
            if self.death_timer % 3 == 0:
                pygame.draw.circle(surf, (255, 200, 50), (sx, sy - 12), 10)
                pygame.draw.circle(surf, (255, 100, 0), (sx, sy - 12), 6)
            return
        draw = pygame.transform.flip(self.sprite, self.facing == 1, False)
        surf.blit(draw, (sx - 16, sy - 12))
