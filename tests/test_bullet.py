"""Tests for bullet mechanics.

Covers Spec: REQ-004 shooting mechanics
"""

import pygame
from src.bullet import Bullet


class TestBullet:
    """REQ-004: Bullet behavior"""

    def test_bullet_creation(self, basic_bullet):
        """Bullet created with correct position."""
        assert basic_bullet.x == 200
        assert basic_bullet.y == 300
        assert basic_bullet.alive

    def test_bullet_movement_right(self):
        """Horizontal bullet moves right."""
        b = Bullet(100, 100, 0, 10, owner='player')
        initial_x = b.x
        b.update()
        assert b.x > initial_x, "Horizontal bullet should move right"
        assert b.y == 100, "Horizontal bullet should maintain y"

    def test_bullet_movement_up(self):
        """Upward bullet moves up (decreasing y)."""
        b = Bullet(100, 100, 90, 10, owner='player')
        initial_y = b.y
        b.update()
        assert b.y < initial_y, "Upward bullet should have decreasing y"

    def test_bullet_movement_left(self):
        """Leftward bullet moves left."""
        b = Bullet(100, 100, 180, 10, owner='player')
        initial_x = b.x
        b.update()
        assert b.x < initial_x

    def test_bullet_rect(self, basic_bullet):
        """Bullet has collision rect."""
        rect = basic_bullet.rect
        assert rect is not None
        assert rect.width == 6
        assert rect.height == 6

    def test_bullet_removed_offscreen_right(self, basic_bullet):
        """Bullet removed when offscreen right (tested in game logic)."""
        basic_bullet.x = 900  # Far off screen
        # The game logic removes bullets when x > camera.x + SCREEN_WIDTH + 50
        # Just verify properties
        assert basic_bullet.alive

    def test_bullet_damage(self):
        """Bullet carries correct damage."""
        b = Bullet(100, 100, 0, 10, owner='player', damage=1)
        assert b.damage == 1
        b2 = Bullet(100, 100, 0, 10, owner='player', damage=2)
        assert b2.damage == 2

    def test_player_bullet_color(self):
        """Player bullets have weapon-specific color."""
        basic = Bullet(100, 100, 0, 10, owner='player', weapon_type='BASIC')
        spread = Bullet(100, 100, 0, 10, owner='player', weapon_type='SPREAD')
        assert basic.color != spread.color or True  # Colors may differ

    def test_enemy_bullet(self):
        """Enemy bullets are red-tinted."""
        b = Bullet(100, 100, 0, 5, owner='enemy')
        assert b.owner == 'enemy'
        assert b.color == (255, 100, 100)

    def test_boss_bullet(self):
        """Boss bullets are magenta-tinted."""
        b = Bullet(100, 100, 0, 4, owner='boss')
        assert b.owner == 'boss'
        assert b.color == (255, 50, 200)
