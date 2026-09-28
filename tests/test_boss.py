"""Tests for boss behavior.

Covers Spec: REQ-014 boss system
"""

import math


class TestJungleBoss:
    """REQ-014.2: Jungle Boss"""

    def test_boss_creation(self, jungle_boss):
        """Boss created at correct position with correct HP."""
        assert jungle_boss.x == 4600
        assert jungle_boss.y == 360
        assert jungle_boss.max_hp == 20
        assert jungle_boss.hp == 20

    def test_boss_initial_state(self, jungle_boss):
        """Boss starts inactive and alive."""
        assert not jungle_boss.active
        assert jungle_boss.alive

    def test_boss_activation(self, jungle_boss):
        """REQ-014.1: Boss can be activated."""
        jungle_boss.activate()
        assert jungle_boss.active

    def test_boss_take_damage(self, jungle_boss):
        """REQ-014.4: Boss takes damage when hit."""
        jungle_boss.activate()
        initial_hp = jungle_boss.hp
        jungle_boss.take_damage(1)
        assert jungle_boss.hp == initial_hp - 1

    def test_boss_defeated(self, jungle_boss):
        """REQ-014.5: Boss defeated when HP reaches 0."""
        jungle_boss.activate()
        for _ in range(20):
            defeated = jungle_boss.take_damage(1)
            if defeated:
                break
        assert not jungle_boss.alive
        assert jungle_boss.hp == 0

    def test_boss_does_not_attack_before_activation(self, jungle_boss):
        """Boss does not fire before activation."""
        finished, bullets, summons = jungle_boss.update(1.0, 4500, 360)
        assert len(bullets) == 0, "Should not attack before activation"
        assert not finished

    def test_boss_attack_after_activation(self, jungle_boss):
        """Boss fires after activation."""
        jungle_boss.activate()
        jungle_boss.attack_timer = 0  # Force immediate attack
        finished, bullets, summons = jungle_boss.update(1.0, 4500, 360)
        assert len(bullets) > 0, "Boss should fire after activation"

    def test_boss_spread_shot_count(self, jungle_boss):
        """Boss spread shot fires bullets."""
        # Access private method directly
        bullets = jungle_boss._spread_shot(4500, 360, count=3)
        assert len(bullets) == 3

    def test_boss_rect(self, jungle_boss):
        """Boss has collision rect."""
        rect = jungle_boss.rect
        assert rect is not None
        assert rect.width > 0
        assert rect.height > 0

    def test_boss_does_not_respawn(self, jungle_boss):
        """REQ-014.6: Defeated boss does not respawn."""
        jungle_boss.activate()
        for _ in range(20):
            jungle_boss.take_damage(1)
        assert not jungle_boss.alive
        # After death, update still doesn't make it alive again
        jungle_boss.update(1.0, 4500, 360)
        assert not jungle_boss.alive

    def test_boss_update_not_active_returns_empty(self, jungle_boss):
        """update returns empty lists when not active."""
        finished, bullets, summons = jungle_boss.update(1.0, 4500, 360)
        assert finished is False
        assert bullets == []
        assert summons == []


class TestBaseBoss:
    """REQ-014.3: Base Boss"""

    def test_base_boss_creation(self, base_boss):
        """Base boss has higher HP."""
        assert base_boss.max_hp == 30
        assert base_boss.max_hp > 20  # Higher than jungle boss

    def test_base_boss_half_hp_summon(self, base_boss):
        """Base boss summons minions at half HP."""
        base_boss.activate()
        base_boss.attack_timer = 0
        base_boss.hp = base_boss.max_hp // 2 + 1  # Above half
        _, _, summons = base_boss.update(1.0, 5700, 340)
        assert len(summons) == 0, "Should not summon above half HP"

        base_boss.hp = base_boss.max_hp // 2  # At half
        base_boss.summoned = False  # Reset flag
        base_boss.attack_timer = 0
        finished, bullets, summons = base_boss.update(1.0, 5700, 340)
        if base_boss.attack_pattern == 'spread_shot_and_summon':
            assert len(summons) > 0, "Should summon at half HP"

    def test_base_boss_attack_pattern(self, base_boss):
        """Base boss uses spread_shot_and_summon pattern."""
        assert base_boss.attack_pattern == 'spread_shot_and_summon'


class TestBossDamage:
    """REQ-014.4: Boss damage mechanics"""

    def test_damage_before_activation_ignored(self, jungle_boss):
        """Damage before activation is ignored."""
        initial_hp = jungle_boss.hp
        jungle_boss.take_damage(1)
        assert jungle_boss.hp == initial_hp, "Damage before activation should be ignored"

    def test_boss_hp_bar_update(self, jungle_boss, dummy_screen):
        """Health ratio maintained."""
        jungle_boss.activate()
        jungle_boss.take_damage(10)
        expected_ratio = jungle_boss.hp / jungle_boss.max_hp
        assert expected_ratio == 0.5  # 10/20 = 0.5
