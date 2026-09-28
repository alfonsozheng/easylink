"""Bullet entity."""

import math
import pygame

from src.weapon import WEAPON_CONFIGS


class Bullet:
    """A bullet fired by the player or enemies."""

    def __init__(self, x, y, angle, speed, owner='player',
                 weapon_type='BASIC', damage=1):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.owner = owner
        self.weapon_type = weapon_type
        self.damage = damage
        self.alive = True

        rad = math.radians(angle)
        self.vx = math.cos(rad) * speed
        self.vy = -math.sin(rad) * speed

        config = WEAPON_CONFIGS.get(weapon_type, WEAPON_CONFIGS['BASIC'])
        self.color = config['color']

        if owner == 'enemy' or owner == 'boss':
            self.color = (255, 100, 100) if owner == 'enemy' else (255, 50, 200)

        self.width = 6
        self.height = 6

    @property
    def rect(self):
        return pygame.Rect(self.x - self.width // 2,
                           self.y - self.height // 2,
                           self.width, self.height)

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surf, camera_x):
        sx = int(self.x - camera_x)
        sy = int(self.y)
        if -20 < sx < 820:
            c = self.color
            pygame.draw.rect(surf, c, (sx - 3, sy - 3, 6, 6))
            # Glow
            pygame.draw.rect(surf, (c[0], c[1], min(255, c[2] + 50)),
                             (sx - 2, sy - 2, 4, 4))
