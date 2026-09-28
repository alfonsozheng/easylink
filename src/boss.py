"""Boss entities - jungle boss and base boss."""

import math
import random
import pygame

from src.bullet import Bullet
from assets.sprites import make_jungle_boss_sprite, make_base_boss_sprite


class Boss:
    """Base boss class with common behavior."""

    def __init__(self, boss_data):
        self.x = boss_data['x']
        self.y = boss_data['y']
        self.max_hp = boss_data['hp']
        self.hp = self.max_hp
        self.alive = True
        self.active = False
        self.boss_type = boss_data['type']
        self.attack_pattern = boss_data.get('attack_pattern', 'spread_shot')
        self.attack_timer = 0
        self.attack_interval = 1.5  # seconds between attacks
        self.move_timer = 0
        self.move_dir = 1
        self.width = 60
        self.height = 64
        self.death_timer = 0

        # Sprites
        if self.boss_type == 'jungle_boss':
            self.sprite = make_jungle_boss_sprite(2)
        else:
            self.sprite = make_base_boss_sprite(2)

        # Summoned minions tracking
        self.summoned = False

    @property
    def rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y - self.height,
                           self.width, self.height)

    def activate(self):
        """Start boss fight."""
        self.active = True
        self.attack_timer = self.attack_interval

    def take_damage(self, amount=1):
        if not self.active or not self.alive:
            return False
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.death_timer = 60
            return True  # defeated
        return False  # still alive

    def update(self, dt, player_x, player_y):
        """Update boss state. Returns (dead, bullets, summon_enemies)."""
        if not self.alive:
            self.death_timer -= 1
            finished = self.death_timer <= 0
            return finished, [], []

        if not self.active:
            return False, [], []

        # Movement - gentle side to side
        self.move_timer += dt
        self.x += math.sin(self.move_timer * 1.5) * 1.0

        # Attack timer
        self.attack_timer -= dt
        bullets = []
        summon = []
        if self.attack_timer <= 0:
            self.attack_timer = self.attack_interval
            if self.attack_pattern == 'spread_shot':
                bullets = self._spread_shot(player_x, player_y)
            elif self.attack_pattern == 'spread_shot_and_summon':
                bullets = self._spread_shot(player_x, player_y, count=5)
                if not self.summoned and self.hp <= self.max_hp // 2:
                    summon = ['patrol']
                    self.summoned = True

        return False, bullets, summon

    def _spread_shot(self, player_x, player_y, count=3):
        """Fire spread of bullets toward player."""
        bullets = []
        base_angle = math.degrees(math.atan2(
            -(player_y - (self.y - 20)), player_x - self.x))
        spread = 15
        for i in range(count):
            angle = base_angle + (i - (count - 1) / 2) * spread
            bullets.append(Bullet(
                self.x, self.y - 20, angle, 4,
                owner='boss', weapon_type='BASIC', damage=1))
        return bullets

    def draw(self, surf, camera_x):
        sx = int(self.x - camera_x)
        sy = int(self.y)
        if not self.alive:
            # Death explosion animation
            if self.death_timer > 30:
                # Flash white
                flash = pygame.Surface((self.width, self.height))
                flash.fill((255, 255, 255))
                surf.blit(flash, (sx - self.width // 2, sy - self.height))
            elif self.death_timer > 0:
                if self.death_timer % 4 < 2:
                    size = random.randint(4, 16)
                    colors = [(255, 200, 50), (255, 100, 0), (255, 50, 0)]
                    for _ in range(5):
                        ox = random.randint(-20, 20)
                        oy = random.randint(-20, 20)
                        c = random.choice(colors)
                        pygame.draw.circle(surf, c,
                                           (sx + ox, sy - 32 + oy), size // 2)
            return

        if not self.active:
            # Not yet visible - draw nothing or faint outline
            return

        surf.blit(self.sprite, (sx - 32, sy - 64))
