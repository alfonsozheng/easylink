"""Procedural pixel-art sprite generation for Contra-style game.

All sprites are generated programmatically using pygame.Surface, no external
image files are required.
"""

import math
import pygame

# ── Palette ──────────────────────────────────────────────────────────
COLOR_KEY = (0, 0, 0)  # transparency color key (black background)

# Player palette
PLAYER_SKIN = (220, 180, 120)
PLAYER_SHIRT = (60, 80, 200)
PLAYER_PANTS = (100, 60, 40)
PLAYER_BOOTS = (40, 30, 20)
PLAYER_HAIR = (30, 20, 10)
PLAYER_GUN = (180, 160, 140)
PLAYER_BAND = (200, 60, 60)

# Enemy palette
ENEMY_SKIN = (180, 120, 80)
ENEMY_UNIFORM = (80, 80, 80)
ENEMY_BOOTS = (40, 40, 40)
ENEMY_GUN = (160, 140, 120)

# Boss palette
BOSS_JUNGLE_BODY = (40, 120, 40)
BOSS_JUNGLE_EYE = (255, 80, 80)
BOSS_JUNGLE_ARM = (60, 100, 50)
BOSS_BASE_BODY = (120, 120, 140)
BOSS_BASE_EYE = (255, 60, 60)
BOSS_BASE_ARM = (100, 100, 130)

# Item palette
ITEM_GLOW = (255, 255, 100)
ITEM_S = (255, 200, 0)
ITEM_M = (0, 200, 255)
ITEM_R = (255, 100, 0)
ITEM_1UP = (0, 255, 80)
ITEM_SCORE = (255, 255, 0)

# Bullet palette
BULLET_BASIC = (255, 255, 200)
BULLET_SPREAD = (255, 200, 100)
BULLET_MACHINE = (255, 255, 100)
BULLET_RAPID = (255, 150, 50)
BULLET_ENEMY = (255, 100, 100)
BULLET_BOSS = (255, 50, 200)


def _apply_key(surf):
    surf.set_colorkey(COLOR_KEY)
    return surf.convert_alpha() if surf.get_flags() & pygame.SRCALPHA else surf.convert()


def _pixel(surf, x, y, color, scale=1):
    """Draw a pixel at (x,y) with optional scale."""
    if scale == 1:
        surf.set_at((x, y), color)
    else:
        surf.fill(color, (x * scale, y * scale, scale, scale))


def _draw(surf, pixels, palette, scale=1):
    """Draw a sprite from a list of (x,y,color_key) tuples."""
    for x, y, key in pixels:
        _pixel(surf, x, y, palette.get(key, COLOR_KEY), scale)


# ═════════════════════════════════════════════════════════════════════
#  SPRITE GENERATORS
# ═════════════════════════════════════════════════════════════════════

def _player_standing_pixels():
    """Return pixel data for player standing (16x24 logical)."""
    p = {}
    # Head
    for dx in range(4, 12):
        p[(dx, 0)] = 'skin'
        p[(dx, 1)] = 'skin'
    p[(5, 2)] = p[(10, 2)] = 'skin'
    p[(3, 2)] = p[(12, 2)] = 'skin'
    p[(1, 3)] = p[(14, 3)] = 'skin'
    # Hair
    p[(6, 0)] = p[(7, 0)] = p[(8, 0)] = p[(9, 0)] = 'hair'
    # Eyes
    p[(5, 1)] = p[(10, 1)] = 'hair'
    # Bandana
    p[(6, 1)] = p[(7, 1)] = p[(8, 1)] = p[(9, 1)] = 'band'
    # Body / shirt
    for x in range(4, 12):
        p[(x, 3)] = 'shirt'
        p[(x, 4)] = 'shirt'
        p[(x, 5)] = 'shirt'
        p[(x, 6)] = 'shirt'
    for x in range(3, 13):
        p[(x, 7)] = 'shirt'
    # Arms
    p[(2, 4)] = p[(2, 5)] = 'skin'
    p[(13, 3)] = p[(13, 4)] = 'skin'
    p[(14, 4)] = 'skin'
    # Gun
    p[(15, 3)] = p[(15, 4)] = p[(16, 4)] = 'gun'
    # Pants
    for x in range(5, 11):
        p[(x, 8)] = 'pants'
        p[(x, 9)] = 'pants'
    p[(4, 8)] = p[(11, 8)] = 'pants'
    # Boots
    for x in range(4, 6):
        p[(x, 10)] = 'boots'
    for x in range(10, 12):
        p[(x, 10)] = 'boots'
    p[(9, 10)] = 'boots'
    return p


def _player_prone_pixels():
    """Pixel data for player prone (24x12 logical)."""
    p = {}
    # Body horizontal
    for x in range(4, 20):
        p[(x, 2)] = 'shirt'
        p[(x, 3)] = 'shirt'
    for x in range(3, 5):
        p[(x, 3)] = 'shirt'
    # Head
    for dx in range(0, 4):
        p[(dx, 2)] = 'skin'
        p[(dx, 3)] = 'skin'
    p[(0, 4)] = p[(1, 4)] = 'skin'
    p[(2, 1)] = p[(3, 1)] = 'skin'
    p[(2, 4)] = p[(3, 4)] = 'skin'
    # Hair
    p[(0, 2)] = p[(1, 2)] = 'hair'
    # Bandana
    p[(1, 3)] = p[(2, 3)] = 'band'
    # Gun forward
    for x in range(20, 24):
        p[(x, 3)] = 'gun'
    # Pants
    for x in range(4, 10):
        p[(x, 4)] = 'pants'
    for x in range(16, 20):
        p[(x, 4)] = 'pants'
    # Boots
    p[(4, 5)] = p[(5, 5)] = 'boots'
    p[(18, 5)] = p[(19, 5)] = 'boots'
    # Arms
    p[(20, 2)] = p[(21, 2)] = 'skin'
    return p


def make_player_sprite(scale=2):
    """Create a player standing sprite (16x24 logical → 32x48 at scale=2)."""
    size = (16 * scale, 24 * scale)
    surf = pygame.Surface(size).convert_alpha()
    surf.fill((0, 0, 0, 0))
    palette = {
        'skin': PLAYER_SKIN, 'shirt': PLAYER_SHIRT, 'pants': PLAYER_PANTS,
        'boots': PLAYER_BOOTS, 'hair': PLAYER_HAIR, 'gun': PLAYER_GUN,
        'band': PLAYER_BAND,
    }
    pixels = _player_standing_pixels()
    for (x, y), key in pixels.items():
        px, py = x * scale, y * scale
        surf.fill(palette[key], (px, py, scale, scale))
    return surf


def make_player_prone_sprite(scale=2):
    """Create a player prone sprite (24x12 logical → 48x24 at scale=2)."""
    size = (24 * scale, 16 * scale)
    surf = pygame.Surface(size).convert_alpha()
    surf.fill((0, 0, 0, 0))
    palette = {
        'skin': PLAYER_SKIN, 'shirt': PLAYER_SHIRT, 'pants': PLAYER_PANTS,
        'boots': PLAYER_BOOTS, 'hair': PLAYER_HAIR, 'gun': PLAYER_GUN,
        'band': PLAYER_BAND,
    }
    pixels = _player_prone_pixels()
    for (x, y), key in pixels.items():
        px, py = x * scale, y * scale
        surf.fill(palette[key], (px, py, scale, scale))
    return surf


def _patrol_enemy_pixels():
    p = {}
    # Head
    for dx in range(4, 12):
        p[(dx, 0)] = 'skin'
        p[(dx, 1)] = 'skin'
    p[(6, 0)] = p[(7, 0)] = p[(8, 0)] = p[(9, 0)] = 'hair'
    p[(5, 1)] = p[(10, 1)] = 'hair'
    # Helmet
    for dx in range(3, 13):
        p[(dx, 0)] = 'uniform'
    p[(4, 1)] = p[(11, 1)] = 'uniform'
    # Body
    for x in range(4, 12):
        p[(x, 3)] = p[(x, 4)] = p[(x, 5)] = p[(x, 6)] = 'uniform'
    for x in range(3, 13):
        p[(x, 7)] = 'uniform'
    # Arms
    p[(2, 4)] = p[(2, 5)] = 'skin'
    p[(13, 3)] = p[(13, 4)] = 'skin'
    p[(14, 4)] = 'skin'
    # Gun
    p[(15, 3)] = p[(15, 4)] = p[(16, 4)] = 'gun'
    # Legs
    for x in range(5, 11):
        p[(x, 8)] = p[(x, 9)] = 'uniform'
    p[(4, 8)] = p[(11, 8)] = 'uniform'
    # Boots
    for x in range(4, 6):
        p[(x, 10)] = 'boots'
    for x in range(10, 12):
        p[(x, 10)] = 'boots'
    return p


def make_enemy_patrol_sprite(scale=2):
    """16x24 logical → 32x48."""
    size = (18 * scale, 24 * scale)
    surf = pygame.Surface(size).convert_alpha()
    surf.fill((0, 0, 0, 0))
    palette = {
        'skin': ENEMY_SKIN, 'uniform': ENEMY_UNIFORM,
        'boots': ENEMY_BOOTS, 'gun': ENEMY_GUN, 'hair': (40, 30, 20),
    }
    pixels = _patrol_enemy_pixels()
    for (x, y), key in pixels.items():
        surf.fill(palette[key], (x * scale, y * scale, scale, scale))
    return surf


def _sentry_enemy_pixels():
    p = {}
    # Head
    for dx in range(4, 12):
        p[(dx, 0)] = 'skin'
        p[(dx, 1)] = 'skin'
    # Helmet
    for dx in range(3, 13):
        p[(dx, 0)] = 'uniform'
    p[(4, 1)] = p[(11, 1)] = 'uniform'
    # Body
    for x in range(4, 12):
        p[(x, 2)] = p[(x, 3)] = p[(x, 4)] = 'uniform'
    for x in range(3, 13):
        p[(x, 5)] = 'uniform'
    # Arms with gun pointing up
    p[(13, 2)] = p[(13, 3)] = 'skin'
    p[(14, 1)] = p[(14, 2)] = 'gun'
    p[(2, 2)] = p[(2, 3)] = 'skin'
    # Base/stand
    for x in range(4, 12):
        p[(x, 6)] = p[(x, 7)] = 'boots'
    return p


def make_enemy_sentry_sprite(scale=2):
    """16x12 logical → 32x24."""
    size = (16 * scale, 12 * scale)
    surf = pygame.Surface(size).convert_alpha()
    surf.fill((0, 0, 0, 0))
    palette = {
        'skin': ENEMY_SKIN, 'uniform': ENEMY_UNIFORM,
        'boots': ENEMY_BOOTS, 'gun': ENEMY_GUN,
    }
    pixels = _sentry_enemy_pixels()
    for (x, y), key in pixels.items():
        surf.fill(palette[key], (x * scale, y * scale, scale, scale))
    return surf


def make_jungle_boss_sprite(scale=2):
    """32x32 logical → 64x64."""
    size = (32 * scale, 32 * scale)
    surf = pygame.Surface(size).convert_alpha()
    surf.fill((0, 0, 0, 0))
    # Big mutant plant monster
    # Body
    for x in range(8, 24):
        for y in range(8, 28):
            surf.fill(BOSS_JUNGLE_BODY, (x * scale, y * scale, scale, scale))
    # Eyes
    surf.fill(BOSS_JUNGLE_EYE, (10 * scale, 10 * scale, 3 * scale, 3 * scale))
    surf.fill(BOSS_JUNGLE_EYE, (19 * scale, 10 * scale, 3 * scale, 3 * scale))
    # Arms/tentacles
    for x in range(2, 8):
        for y in range(12, 16):
            surf.fill(BOSS_JUNGLE_ARM, (x * scale, y * scale, scale, scale))
    for x in range(24, 30):
        for y in range(12, 16):
            surf.fill(BOSS_JUNGLE_ARM, (x * scale, y * scale, scale, scale))
    # Mouth
    surf.fill((200, 0, 0), (13 * scale, 22 * scale, 6 * scale, 3 * scale))
    # Teeth
    for tx in [13, 15, 17]:
        surf.fill((255, 255, 255), (tx * scale, 22 * scale, 2 * scale, 2 * scale))
    return surf


def make_base_boss_sprite(scale=2):
    """32x32 logical → 64x64."""
    size = (32 * scale, 36 * scale)
    surf = pygame.Surface(size).convert_alpha()
    surf.fill((0, 0, 0, 0))
    # Large mechanical body
    for x in range(6, 26):
        for y in range(6, 30):
            surf.fill(BOSS_BASE_BODY, (x * scale, y * scale, scale, scale))
    # Armor plates
    for x in range(8, 24):
        for y in range(8, 12):
            surf.fill((80, 80, 100), (x * scale, y * scale, scale, scale))
    for x in range(8, 24):
        for y in range(16, 18):
            surf.fill((80, 80, 100), (x * scale, y * scale, scale, scale))
    # Red eyes
    surf.fill(BOSS_BASE_EYE, (10 * scale, 10 * scale, 3 * scale, 3 * scale))
    surf.fill(BOSS_BASE_EYE, (19 * scale, 10 * scale, 3 * scale, 3 * scale))
    # Weapon cannons (arms)
    for x in range(0, 6):
        for y in range(14, 18):
            surf.fill((80, 80, 100), (x * scale, y * scale, scale, scale))
    for x in range(26, 32):
        for y in range(14, 18):
            surf.fill((80, 80, 100), (x * scale, y * scale, scale, scale))
    # Cannon barrels
    surf.fill((60, 60, 60), (0, 14 * scale, 3 * scale, 4 * scale))
    surf.fill((60, 60, 60), (29 * scale, 14 * scale, 3 * scale, 4 * scale))
    # Legs
    for x in range(8, 12):
        for y in range(30, 36):
            surf.fill(BOSS_BASE_BODY, (x * scale, y * scale, scale, scale))
    for x in range(20, 24):
        for y in range(30, 36):
            surf.fill(BOSS_BASE_BODY, (x * scale, y * scale, scale, scale))
    return surf


def make_bullet_sprite(weapon_type='BASIC', scale=2):
    """Create a bullet sprite (4x4 logical)."""
    colors = {
        'BASIC': BULLET_BASIC,
        'SPREAD': BULLET_SPREAD,
        'MACHINE_GUN': BULLET_MACHINE,
        'RAPID': BULLET_RAPID,
        'ENEMY': BULLET_ENEMY,
        'BOSS': BULLET_BOSS,
    }
    color = colors.get(weapon_type, BULLET_BASIC)
    size = (4 * scale, 4 * scale)
    surf = pygame.Surface(size).convert_alpha()
    surf.fill((0, 0, 0, 0))
    if weapon_type == 'SPREAD':
        # Slightly bigger
        surf.fill(color, (0, 0, 4 * scale, 4 * scale))
    elif weapon_type == 'RAPID':
        surf.fill(color, (0, 0, 4 * scale, 4 * scale))
        # Core
        inner = (scale, scale, 2 * scale, 2 * scale)
        surf.fill((255, 255, 200), inner)
    elif weapon_type == 'ENEMY' or weapon_type == 'BOSS':
        surf.fill(color, (scale // 2, scale // 2, 3 * scale, 3 * scale))
    else:
        surf.fill(color, (scale // 2, scale // 2, 3 * scale, 3 * scale))
    return surf


def make_item_sprite(item_type, scale=2):
    """Create item pickup sprite (16x16 logical)."""
    size = (16 * scale, 16 * scale)
    surf = pygame.Surface(size).convert_alpha()
    surf.fill((0, 0, 0, 0))
    colors = {
        'weapon_S': ITEM_S,
        'weapon_M': ITEM_M,
        'weapon_R': ITEM_R,
        '1UP': ITEM_1UP,
        'score': ITEM_SCORE,
    }
    labels = {
        'weapon_S': 'S', 'weapon_M': 'M', 'weapon_R': 'R',
        '1UP': '1UP', 'score': '500',
    }
    color = colors.get(item_type, ITEM_GLOW)
    label = labels.get(item_type, '?')

    # Glow background
    cx, cy = 8 * scale, 8 * scale
    r = 6 * scale
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                alpha = max(0, 64 - int(math.sqrt(dx * dx + dy * dy)) * 8)
                surf.set_at((cx + dx, cy + dy), (*color[:3], alpha))

    # Background box
    surf.fill((50, 50, 50), (3 * scale, 3 * scale, 10 * scale, 10 * scale))
    surf.fill(color, (4 * scale, 4 * scale, 8 * scale, 8 * scale))

    return surf, label


def make_particle_surf(color, size):
    """Create a small particle surface."""
    surf = pygame.Surface(size).convert_alpha()
    surf.fill((0, 0, 0, 0))
    pygame.draw.circle(surf, color, (size[0] // 2, size[1] // 2), size[0] // 2)
    return surf


def make_platform_tile(theme='jungle', scale=2):
    """Create a ground/platform tile."""
    size = (16 * scale, 16 * scale)
    surf = pygame.Surface(size).convert_alpha()
    surf.fill((0, 0, 0, 0))
    if theme == 'jungle':
        top_color = (60, 140, 40)
        fill_color = (80, 100, 40)
        detail_color = (60, 80, 30)
    else:  # base
        top_color = (120, 120, 130)
        fill_color = (100, 100, 110)
        detail_color = (80, 80, 90)

    surf.fill(fill_color, (0, 0, size[0], size[1]))
    # Top edge (grass or metal)
    surf.fill(top_color, (0, 0, size[0], 3 * scale))
    # Detail lines
    for y in range(4, size[1] // scale, 4):
        surf.fill(detail_color, (0, y * scale, size[0], scale))
    return surf


def make_ladder_tile(scale=2):
    """Create a ladder tile."""
    size = (16 * scale, 16 * scale)
    surf = pygame.Surface(size).convert_alpha()
    surf.fill((0, 0, 0, 0))
    # Rails
    surf.fill((120, 100, 80), (2 * scale, 0, 2 * scale, size[1]))
    surf.fill((120, 100, 80), (12 * scale, 0, 2 * scale, size[1]))
    # Rungs
    for y in range(0, size[1] // scale, 4):
        surf.fill((160, 140, 100), (2 * scale, y * scale, 12 * scale, scale))
    return surf


def make_bg_layer(theme='jungle', width=800, height=600):
    """Create a background surface."""
    surf = pygame.Surface((width, height)).convert()
    if theme == 'jungle':
        # Sky gradient
        for y in range(height):
            r = int(40 + y * 0.02)
            g = int(60 + y * 0.05)
            b = int(80 + y * 0.02)
            surf.fill((min(r, 80), min(g, 120), min(b, 100)), (0, y, width, 1))
        # Some trees in background
        for tx in range(0, width, 120):
            tree_color = (30, 70, 30)
            # Trunk
            surf.fill((60, 40, 20), (tx + 8, 300, 6, 200))
            # Foliage
            for fy in range(280, 320, 8):
                for fx in range(tx, tx + 20, 4):
                    surf.fill(tree_color, (fx, fy, 4, 4))
    else:  # base
        for y in range(height):
            gray = int(60 + y * 0.03)
            surf.fill((min(gray, 100), min(gray, 100), min(gray + 20, 130)),
                      (0, y, width, 1))
        # Some structural lines
        for sy in range(0, height, 60):
            surf.fill((80, 80, 100), (0, sy, width, 1))
    return surf
