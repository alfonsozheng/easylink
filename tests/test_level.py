"""Tests for level loading and management.

Covers Spec: REQ-011, REQ-012 level data
"""

import pygame


class TestLevel1:
    """REQ-011: Level 1 - Jungle"""

    def test_level1_loaded(self, level1):
        """REQ-011.1: Level 1 loads successfully."""
        assert level1 is not None
        assert level1.level_id == 1

    def test_level1_theme(self, level1):
        """Level 1 is jungle theme."""
        assert level1.theme == 'jungle'

    def test_level1_width(self, level1):
        """Level 1 has appropriate width."""
        assert level1.level_width == 6400

    def test_level1_has_terrain(self, level1):
        """REQ-011.2: Level 1 has terrain."""
        assert len(level1.terrain_rects) > 0

    def test_level1_has_ladders(self, level1):
        """REQ-011.2: Level 1 has ladders."""
        assert len(level1.ladder_rects) > 0

    def test_level1_has_pits(self, level1):
        """REQ-011.2: Level 1 has pits/gaps."""
        pit_count = sum(1 for t in level1.data.get('terrain', [])
                       if t['type'] == 'pit')
        assert pit_count >= 1

    def test_level1_enemies(self, level1):
        """REQ-011.3: Level 1 has enemies."""
        assert len(level1.enemies) >= 5

    def test_level1_items(self, level1):
        """REQ-011.4: Level 1 has weapon items."""
        assert len(level1.items) >= 2

    def test_level1_has_boss(self, level1):
        """REQ-011.5: Level 1 has boss."""
        assert level1.boss is not None
        assert level1.boss.boss_type == 'jungle_boss'

    def test_level1_spawn_point(self, level1):
        """Level 1 has player spawn."""
        assert level1.player_spawn is not None
        assert level1.player_spawn[0] > 0

    def test_level1_enemy_types(self, level1):
        """Level 1 has both patrol and sentry enemies."""
        has_patrol = any(e.__class__.__name__ == 'PatrolEnemy'
                        for e in level1.enemies)
        has_sentry = any(e.__class__.__name__ == 'SentryEnemy'
                        for e in level1.enemies)
        assert has_patrol, "Level 1 should have patrol enemies"
        assert has_sentry, "Level 1 should have sentry enemies"


class TestLevel2:
    """REQ-012: Level 2 - Military Base"""

    def test_level2_loaded(self, level2):
        """REQ-012.1: Level 2 loads successfully."""
        assert level2 is not None
        assert level2.level_id == 2

    def test_level2_theme(self, level2):
        """Level 2 is base theme."""
        assert level2.theme == 'base'

    def test_level2_width_larger(self, level2):
        """REQ-012.2: Level 2 is wider or equal to level 1."""
        assert level2.level_width >= 6400

    def test_level2_has_terrain(self, level2):
        """Level 2 has terrain elements."""
        assert len(level2.terrain_rects) > 0

    def test_level2_has_ladders(self, level2):
        """Level 2 has ladders."""
        assert len(level2.ladder_rects) >= 2

    def test_level2_has_pits(self, level2):
        """Level 2 has pits."""
        pit_count = sum(1 for t in level2.data.get('terrain', [])
                       if t['type'] == 'pit')
        assert pit_count >= 2

    def test_level2_enemies_more_than_level1(self, level2, level1):
        """REQ-012.7: Level 2 has more enemies than level 1."""
        assert len(level2.enemies) > len(level1.enemies)

    def test_level2_items(self, level2):
        """REQ-012.4: Level 2 has weapon items."""
        assert len(level2.items) >= 3

    def test_level2_has_boss(self, level2):
        """REQ-012.5: Level 2 has boss."""
        assert level2.boss is not None
        assert level2.boss.boss_type == 'base_boss'

    def test_level2_boss_higher_hp(self, level2, level1):
        """Level 2 boss has higher HP."""
        assert level2.boss.max_hp > level1.boss.max_hp

    def test_level2_enemy_density(self, level2, level1):
        """Level 2 has higher enemy density than level 1."""
        density1 = len(level1.enemies) / level1.level_width
        density2 = len(level2.enemies) / level2.level_width
        assert density2 > density1, "Level 2 should have higher enemy density"


class TestLevelMechanics:
    """Level loading and mechanics"""

    def test_boss_trigger_x(self, level1):
        """Boss trigger position exists."""
        trigger_x = level1.get_boss_trigger_x()
        assert trigger_x > 0
        assert trigger_x < level1.level_width

    def test_activate_boss(self, level1):
        """Boss activation works."""
        result = level1.activate_boss()
        assert result
        assert level1.boss.active

    def test_activate_boss_twice(self, level1):
        """Second activation returns False."""
        level1.activate_boss()
        result = level1.activate_boss()
        assert not result, "Second activation should return False"

    def test_draw_background(self, level1, dummy_screen):
        """Background rendering doesn't crash."""
        level1.draw_background(dummy_screen, 0)
        # Should have drawn something
        assert dummy_screen is not None

    def test_draw_terrain(self, level1, dummy_screen):
        """Terrain rendering doesn't crash."""
        level1.draw_terrain(dummy_screen, 0)
        assert dummy_screen is not None
