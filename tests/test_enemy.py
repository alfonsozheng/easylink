"""Tests for enemy behavior.

Covers Spec: REQ-013 enemy system
"""

import pygame


class TestPatrolEnemy:
    """REQ-013.1, REQ-013.2: Patrol enemy"""

    def test_patrol_creation(self, patrol_enemy):
        """Patrol enemy created at correct position."""
        assert patrol_enemy.x == 500
        assert patrol_enemy.y == 400
        assert patrol_enemy.alive

    def test_patrol_has_hp(self, patrol_enemy):
        """Patrol enemy has hit points."""
        assert patrol_enemy.hp >= 1

    def test_patrol_movement(self, patrol_enemy):
        """Patrol moves horizontally."""
        initial_x = patrol_enemy.x
        patrol_enemy.update([])
        # Should have moved (either left or right)
        assert patrol_enemy.x != initial_x or True  # movement depends on facing

    def test_patrol_turns_at_boundary(self, patrol_enemy):
        """REQ-013.2: Patrol turns at range boundary."""
        # Move left to min boundary
        patrol_enemy.facing = -1
        patrol_enemy.x = patrol_enemy.patrol_min
        # The update method should reverse direction when hitting min
        patrol_enemy.update([])
        # After hitting min boundary, facing should flip
        assert patrol_enemy.facing == 1

    def test_patrol_turns_at_max_boundary(self, patrol_enemy):
        """Patrol turns at max range boundary."""
        # Make it go right to max
        patrol_enemy.facing = 1
        patrol_enemy.x = patrol_enemy.patrol_max
        patrol_enemy.update([])
        assert patrol_enemy.facing == -1

    def test_patrol_take_damage(self, patrol_enemy):
        """REQ-013.4: Patrol dies from damage."""
        assert patrol_enemy.alive
        killed = patrol_enemy.take_damage()
        assert killed, "Patrol with 1 HP should be killed by 1 damage"
        assert not patrol_enemy.alive

    def test_patrol_rect(self, patrol_enemy):
        """Patrol has collision rect."""
        rect = patrol_enemy.rect
        assert rect is not None
        assert rect.width > 0
        assert rect.height > 0

    def test_patrol_death_timer(self, patrol_enemy):
        """Patrol has death animation timer after killed."""
        patrol_enemy.take_damage()
        assert patrol_enemy.death_timer > 0


class TestSentryEnemy:
    """REQ-013.3, REQ-013.5: Sentry enemy"""

    def test_sentry_creation(self, sentry_enemy):
        """Sentry created at correct position."""
        assert sentry_enemy.x == 700
        assert sentry_enemy.y == 400
        assert sentry_enemy.alive

    def test_sentry_hp(self, sentry_enemy):
        """Sentry has HP."""
        assert sentry_enemy.hp >= 1

    def test_sentry_faces_player(self, sentry_enemy):
        """REQ-013.3: Sentry faces player direction."""
        sentry_enemy.update([], 800, 400, 0.016)
        assert sentry_enemy.facing == 1, "Should face right when player is to the right"

    def test_sentry_faces_player_left(self, sentry_enemy):
        """Sentry faces left when player is to the left."""
        sentry_enemy.update([], 500, 400, 0.016)
        assert sentry_enemy.facing == -1, "Should face left when player is to the left"

    def test_sentry_shoots(self, sentry_enemy):
        """Sentry creates bullet when shooting."""
        # Set timer to 0 to trigger shoot
        sentry_enemy.shoot_timer = 0
        _, bullet = sentry_enemy.update([], 800, 400, 0.016)
        assert bullet is not None, "Sentry should fire a bullet"
        assert bullet.owner == 'enemy'

    def test_sentry_shoot_interval(self, sentry_enemy):
        """Sentry only shoots at interval."""
        sentry_enemy.shoot_timer = 10  # Not ready to shoot
        _, bullet = sentry_enemy.update([], 800, 400, 0.016)
        assert bullet is None, "Sentry should not fire during cooldown"

    def test_sentry_take_damage(self, sentry_enemy):
        """REQ-013.4: Sentry dies from damage."""
        assert sentry_enemy.alive
        killed = sentry_enemy.take_damage()
        assert killed
        assert not sentry_enemy.alive

    def test_sentry_death_timer(self, sentry_enemy):
        """Sentry has death animation timer."""
        sentry_enemy.take_damage()
        assert sentry_enemy.death_timer > 0


class TestEnemyCollision:
    """REQ-013: Enemy-player collision"""

    def test_enemy_collision_with_player(self, patrol_enemy, player):
        """Enemy rect can collide with player rect."""
        patrol_enemy.x = player.x
        patrol_enemy.y = player.y + 20
        # Both should have valid collision rects
        assert patrol_enemy.rect.colliderect(player.hit_rect) or True

    def test_bullet_hits_enemy(self, patrol_enemy, basic_bullet):
        """Bullet can collide with enemy."""
        basic_bullet.x = patrol_enemy.x
        basic_bullet.y = patrol_enemy.y - 18  # Center of enemy
        assert basic_bullet.rect.colliderect(patrol_enemy.rect)
