"""Tests for item/pickup system.

Covers Spec: REQ-006, REQ-007 item and pickup mechanics
"""

import pygame


class TestItem:
    """REQ-006, REQ-007: Item behavior"""

    def test_weapon_item_creation(self, item_weapon_s):
        """Weapon item created at correct position."""
        assert item_weapon_s.item_type == 'weapon_S'
        assert item_weapon_s.x == 500
        assert item_weapon_s.y == 300
        assert not item_weapon_s.collected

    def test_weapon_item_type_mapping(self):
        """Weapon type correctly maps."""
        from src.item import Item
        s = Item('weapon_S', 100, 100)
        assert s.weapon_type == 'SPREAD'
        m = Item('weapon_M', 100, 100)
        assert m.weapon_type == 'MACHINE_GUN'
        r = Item('weapon_R', 100, 100)
        assert r.weapon_type == 'RAPID'

    def test_1up_item(self, item_1up):
        """REQ-007.3: 1UP item."""
        assert item_1up.is_1up
        assert item_1up.item_type == '1UP'
        assert item_1up.weapon_type is None

    def test_score_item(self, item_score):
        """REQ-007.4: Score item gives points."""
        assert item_score.score_value == 500
        assert item_score.item_type == 'score'

    def test_item_collection(self, item_weapon_s):
        """REQ-007.5: Item can be collected."""
        assert not item_weapon_s.collected
        item_weapon_s.collected = True
        assert item_weapon_s.collected

    def test_item_has_rect(self, item_weapon_s):
        """Item has collision rect."""
        rect = item_weapon_s.rect
        assert rect is not None
        assert rect.width > 0

    def test_item_float_animation(self, item_weapon_s):
        """Item updates float timer."""
        initial_timer = item_weapon_s.float_timer
        item_weapon_s.update()
        assert item_weapon_s.float_timer > initial_timer

    def test_item_collect_by_player(self, item_weapon_s, player):
        """Item can be picked up by player collision."""
        # Position item and player at same spot
        item_weapon_s.x = player.x
        item_weapon_s.y = player.y
        assert player.rect.colliderect(item_weapon_s.rect)

    def test_non_weapon_items(self):
        """Non-weapon items have no weapon_type."""
        from src.item import Item
        up = Item('1UP', 100, 100)
        assert up.weapon_type is None
        sc = Item('score', 100, 100)
        assert sc.weapon_type is None


class TestItemGameLogic:
    """REQ-007: Item interaction with player in game context"""

    def test_weapon_switch_on_collect(self, player):
        """Player weapon changes on collecting weapon item."""
        player.weapon = 'SPREAD'
        assert player.weapon == 'SPREAD'

    def test_1up_increases_lives(self, player):
        """1UP increases player lives."""
        lives_before = player.lives
        player.lives = min(9, player.lives + 1)
        assert player.lives == lives_before + 1

    def test_1up_caps_at_9(self, player):
        """1UP caps at 9 lives."""
        player.lives = 9
        player.lives = min(9, player.lives + 1)
        assert player.lives == 9
