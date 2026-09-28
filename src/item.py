"""Item/pickup entities."""

import math
import random
import pygame

from assets.sprites import make_item_sprite


class Item:
    """Collectible item on the map."""

    def __init__(self, item_type, x, y):
        self.item_type = item_type  # 'weapon_S', 'weapon_M', 'weapon_R', '1UP', 'score'
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.collected = False
        self.float_timer = random.uniform(0, math.pi * 2)
        self.base_y = y
        self.sprite, self.label = make_item_sprite(item_type, 2)

    @property
    def rect(self):
        return pygame.Rect(self.x - self.width // 2,
                           self.y - self.height // 2,
                           self.width, self.height)

    @property
    def weapon_type(self):
        mapping = {
            'weapon_S': 'SPREAD',
            'weapon_M': 'MACHINE_GUN',
            'weapon_R': 'RAPID',
        }
        return mapping.get(self.item_type)

    @property
    def score_value(self):
        if self.item_type == 'score':
            return 500
        return 0

    @property
    def is_1up(self):
        return self.item_type == '1UP'

    def update(self):
        self.float_timer += 0.05

    def draw(self, surf, camera_x):
        if self.collected:
            return
        sx = int(self.x - camera_x)
        sy = int(self.base_y + math.sin(self.float_timer) * 4)
        surf.blit(self.sprite, (sx - 16, sy - 16))
        font = pygame.font.Font(None, 14)
        label_surf = font.render(self.label, True, (255, 255, 255))
        surf.blit(label_surf, (sx - 4, sy - 4))
