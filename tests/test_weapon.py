"""Tests for weapon configurations.

Covers Spec: REQ-006 weapon system
"""

from src.weapon import WEAPON_CONFIGS, WEAPON_ORDER


class TestWeaponConfigs:
    """REQ-006: Weapon configuration correctness"""

    def test_weapon_count(self):
        """At least 4 weapon types."""
        assert len(WEAPON_CONFIGS) >= 4

    def test_basic_weapon_exists(self):
        """BASIC weapon exists."""
        assert 'BASIC' in WEAPON_CONFIGS

    def test_spread_weapon_exists(self):
        """SPREAD weapon exists."""
        assert 'SPREAD' in WEAPON_CONFIGS

    def test_machine_gun_exists(self):
        """MACHINE_GUN weapon exists."""
        assert 'MACHINE_GUN' in WEAPON_CONFIGS

    def test_rapid_weapon_exists(self):
        """RAPID weapon exists."""
        assert 'RAPID' in WEAPON_CONFIGS

    def test_all_weapons_have_name(self):
        """All weapons have a name."""
        for key, config in WEAPON_CONFIGS.items():
            assert 'name' in config, f"{key} missing 'name'"

    def test_all_weapons_have_bullet_speed(self):
        """All weapons have bullet_speed."""
        for key, config in WEAPON_CONFIGS.items():
            assert 'bullet_speed' in config, f"{key} missing 'bullet_speed'"
            assert isinstance(config['bullet_speed'], (int, float))

    def test_all_weapons_have_fire_rate(self):
        """All weapons have fire_rate."""
        for key, config in WEAPON_CONFIGS.items():
            assert 'fire_rate' in config, f"{key} missing 'fire_rate'"

    def test_all_weapons_have_spread_count(self):
        """All weapons have spread_count."""
        for key, config in WEAPON_CONFIGS.items():
            assert 'spread_count' in config, f"{key} missing 'spread_count'"

    def test_all_weapons_have_damage(self):
        """All weapons have damage."""
        for key, config in WEAPON_CONFIGS.items():
            assert 'damage' in config, f"{key} missing 'damage'"

    def test_all_weapons_have_color(self):
        """All weapons have a color tuple."""
        for key, config in WEAPON_CONFIGS.items():
            assert 'color' in config, f"{key} missing 'color'"
            assert len(config['color']) == 3

    def test_basic_single_shot(self):
        """BASIC fires single bullet."""
        assert WEAPON_CONFIGS['BASIC']['spread_count'] == 1

    def test_spread_multiple(self):
        """SPREAD fires multiple."""
        assert WEAPON_CONFIGS['SPREAD']['spread_count'] >= 3

    def test_machine_gun_fast_rate(self):
        """MACHINE_GUN has fastest fire rate (lowest number)."""
        rates = {k: v['fire_rate'] for k, v in WEAPON_CONFIGS.items()}
        assert rates['MACHINE_GUN'] <= min(rates.values())

    def test_rapid_highest_damage(self):
        """RAPID has highest damage among weapons."""
        damages = {k: v['damage'] for k, v in WEAPON_CONFIGS.items()}
        assert damages['RAPID'] >= max(damages.values())

    def test_weapon_order_complete(self):
        """WEAPON_ORDER contains all weapons."""
        assert set(WEAPON_ORDER) == set(WEAPON_CONFIGS.keys())
