"""Player character module."""

import math
import pygame

from src.weapon import WEAPON_CONFIGS, WEAPON_ORDER
from src.bullet import Bullet
from assets.sprites import make_player_sprite, make_player_prone_sprite


GRAVITY = 0.6
JUMP_VEL = -10
MOVE_SPEED = 4
MAX_FALL = 12


class Player:
    """Player character with movement, jumping, shooting, and stance."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = 20
        self.height = 40
        self.facing = 1  # 1=right, -1=left
        self.stance = 'STANDING'  # STANDING, PRONE, AIMING_UP
        self.on_ground = False
        self.on_ladder = False
        self.lives = 3
        self.weapon = 'BASIC'
        self.invincible = False
        self.invincible_timer = 0
        self.fire_cooldown = 0
        self.alive = True
        self.respawn_x = x
        self.respawn_y = y

        self.stand_sprite = make_player_sprite(2)
        self.prone_sprite = make_player_prone_sprite(2)

    @property
    def rect(self):
        if self.stance == 'PRONE':
            return pygame.Rect(self.x - 12, self.y - 8, 24, 16)
        return pygame.Rect(self.x - 10, self.y - 20, 20, 20)

    @property
    def hit_rect(self):
        """Collision rect for damage detection."""
        if self.stance == 'PRONE':
            return pygame.Rect(self.x - 10, self.y - 6, 20, 12)
        return pygame.Rect(self.x - 8, self.y - 18, 16, 18)

    def set_respawn(self, x, y):
        self.respawn_x = x
        self.respawn_y = y

    def respawn(self):
        self.x = self.respawn_x
        self.y = self.respawn_y
        self.vx = 0
        self.vy = 0
        self.alive = True
        self.on_ground = False
        self.stance = 'STANDING'
        self.invincible = True
        self.invincible_timer = 90  # ~1.5 seconds at 60fps

    def handle_input(self, keys):
        if not self.alive:
            return

        self.vx = 0

        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -MOVE_SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = MOVE_SPEED
            self.facing = 1

        # Stance (only on ground, not on ladder)
        if self.on_ground and not self.on_ladder:
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.stance = 'PRONE'
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                self.stance = 'AIMING_UP'
            else:
                self.stance = 'STANDING'
        elif self.on_ladder:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.vy = -MOVE_SPEED
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.vy = MOVE_SPEED
            else:
                self.vy = 0

        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] and not
            (keys[pygame.K_DOWN] or keys[pygame.K_s])):
            if self.on_ground and not self.on_ladder:
                self.vy = JUMP_VEL
                self.on_ground = False
                return True  # jump occurred
        return False

    def start_fire(self):
        """Return a list of Bullets if firing, or empty list."""
        if self.fire_cooldown > 0 or not self.alive:
            return []

        config = WEAPON_CONFIGS.get(self.weapon, WEAPON_CONFIGS['BASIC'])
        self.fire_cooldown = config['fire_rate']

        bullets = []
        spread_count = config['spread_count']
        spread_angle = config['spread_angle']

        # Determine base angle
        if self.stance == 'AIMING_UP' or self.stance == 'PRONE':
            base_angle = 90  # shoot upward
        else:
            base_angle = 0 if self.facing == 1 else 180

        for i in range(spread_count):
            if spread_count == 1:
                angle = base_angle
            else:
                offset = (i - (spread_count - 1) / 2) * spread_angle
                angle = base_angle + offset

            bx = self.x + self.facing * 12
            by = self.y - 12 if self.stance != 'PRONE' else self.y - 4
            bullet = Bullet(bx, by, angle, config['bullet_speed'],
                            owner='player', weapon_type=self.weapon,
                            damage=config['damage'])
            bullets.append(bullet)

        return bullets

    def update(self, terrain_rects, ladder_rects):
        if not self.alive:
            return

        # Cooldown
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        # Invincibility
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        # Gravity (only if not on ladder)
        if not self.on_ladder:
            self.vy += GRAVITY
            if self.vy > MAX_FALL:
                self.vy = MAX_FALL
        else:
            # On ladder: minimal gravity
            if abs(self.vy) < 1:
                self.vy = 0.3

        # Move X
        self.x += self.vx
        # Check terrain collision X
        self.on_ground = False
        self.on_ladder = False
        for rect in terrain_rects:
            if self.rect.colliderect(rect):
                if self.vx > 0:
                    self.x = rect.left - self.rect.width // 2 - 5
                elif self.vx < 0:
                    self.x = rect.right + self.rect.width // 2 + 5
                self.vx = 0

        # Move Y
        self.y += self.vy
        # Check terrain collision Y
        for rect in terrain_rects:
            if self.rect.colliderect(rect):
                if self.vy > 0:
                    self.y = rect.top - 10
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.y = rect.bottom + 20
                    self.vy = 0

        # Check ladder collision
        for lrect in ladder_rects:
            if self.rect.colliderect(lrect):
                self.on_ladder = True

        # Keep in level bounds
        if self.y > 500:
            self.alive = False

    def draw(self, surf, camera_x):
        sx = int(self.x - camera_x)
        sy = int(self.y)

        # Flash during invincibility
        if self.invincible and (self.invincible_timer // 6) % 2 == 0:
            return  # skip drawing to create flash effect

        if self.stance == 'PRONE':
            sprite = self.prone_sprite
            offset_y = 8
        else:
            sprite = self.stand_sprite
            offset_y = 20

        draw_surf = pygame.transform.flip(sprite, self.facing == -1, False)
        surf.blit(draw_surf, (sx - 16, sy - offset_y))
