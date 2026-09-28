"""Level loading and management."""

import json
import os
import pygame

from src.enemy import PatrolEnemy, SentryEnemy
from src.boss import Boss
from src.item import Item
from assets.sprites import make_platform_tile, make_ladder_tile, make_bg_layer


class Level:
    """Represents a game level loaded from JSON data."""

    def __init__(self, level_file):
        self.data = self._load(level_file)
        self.level_id = self.data['level_id']
        self.theme = self.data.get('theme', 'jungle')
        self.level_width = self.data.get('level_width', 4800)

        # Build terrain rects
        self.terrain_rects = []
        self.ladder_rects = []
        self._build_terrain()

        # Create enemies
        self.enemies = []
        self._build_enemies()

        # Create items
        self.items = []
        self._build_items()

        # Create boss
        self.boss = None
        if self.data.get('boss'):
            self.boss = Boss(self.data['boss'])

        # Background
        self.bg_surf = make_bg_layer(self.theme, 800, 600)

        # Player spawn
        spawn = self.data.get('player_spawn', {'x': 50, 'y': 300})
        self.player_spawn = (spawn['x'], spawn['y'])

        # Platform/ladder tiles for rendering
        self.platform_tile = make_platform_tile(self.theme, 2)
        self.ladder_tile = make_ladder_tile(2)

    def _load(self, level_file):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, 'levels', level_file)
        with open(path, 'r') as f:
            return json.load(f)

    def _build_terrain(self):
        for t in self.data.get('terrain', []):
            ttype = t['type']
            x, y = t['x'], t['y']
            if ttype == 'platform':
                w, h = t['width'], t['height']
                self.terrain_rects.append(pygame.Rect(x, y, w, h))
            elif ttype == 'step':
                w, h = t['width'], t['height']
                self.terrain_rects.append(pygame.Rect(x, y, w, h))
            elif ttype == 'ladder':
                h = t['height']
                self.ladder_rects.append(pygame.Rect(x, y, 20, h))
            elif ttype == 'pit':
                w = t['width']
                # Pits are just gaps in terrain - visualized as empty space

    def _build_enemies(self):
        for e in self.data.get('enemies', []):
            etype = e['type']
            x, y = e['x'], e['y']
            if etype == 'patrol':
                pr = e.get('patrol_range', [x - 100, x + 100])
                self.enemies.append(PatrolEnemy(x, y, pr))
            elif etype == 'sentry':
                si = e.get('shoot_interval', 1.5)
                self.enemies.append(SentryEnemy(x, y, si))

    def _build_items(self):
        for item_data in self.data.get('items', []):
            self.items.append(Item(item_data['type'],
                                   item_data['x'], item_data['y']))

    def activate_boss(self):
        """Activate the boss when player reaches trigger area."""
        if self.boss and not self.boss.active:
            self.boss.activate()
            return True
        return False

    def get_boss_trigger_x(self):
        """X position where boss activates."""
        if self.data.get('boss'):
            return self.data['boss']['x'] - 200
        return self.level_width

    def draw_background(self, surf, camera_x):
        """Draw scrolling background."""
        # Tile background
        for x in range(-(int(camera_x) % 800), 800, 800 if camera_x < 800 else 800):
            surf.blit(self.bg_surf, (x, 0))
        # Also draw the adjacent tile
        offset = -(int(camera_x) % 800)
        if offset < 0:
            offset += 800
        surf.blit(self.bg_surf, (offset, 0))
        surf.blit(self.bg_surf, (offset - 800, 0))

    def draw_terrain(self, surf, camera_x):
        """Draw terrain platforms and ladders."""
        tile_w = self.platform_tile.get_width()
        tile_h = self.platform_tile.get_height()

        for rect in self.terrain_rects:
            sx = int(rect.x - camera_x)
            # Tile the platform
            for tx in range(0, rect.width, tile_w):
                for ty in range(0, rect.height, tile_h):
                    surf.blit(self.platform_tile, (sx + tx, rect.y + ty))

        for rect in self.ladder_rects:
            sx = int(rect.x - camera_x)
            for ty in range(0, rect.height, tile_h):
                surf.blit(self.ladder_tile, (sx, rect.y + ty))

        # Draw pit indicators (gaps)
        for t in self.data.get('terrain', []):
            if t['type'] == 'pit':
                sx = int(t['x'] - camera_x)
                sy = t['y']
                # Draw danger lines
                for dx in range(0, t['width'], 8):
                    c = (200, 50, 50) if (dx // 8) % 2 == 0 else (100, 20, 20)
                    pygame.draw.line(surf, c, (sx + dx, sy), (sx + dx, sy + 20), 2)
