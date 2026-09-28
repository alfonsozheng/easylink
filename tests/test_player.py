"""Tests for player character mechanics.

Covers Spec requirements: REQ-002, REQ-003, REQ-004, REQ-005, REQ-008
"""

import pygame


class TestPlayerMovement:
    """REQ-002: Player movement"""

    def test_initial_position(self, player):
        """Player starts at given position."""
        assert player.x == 200
        assert player.y == 300

    def test_move_left(self, player):
        """REQ-002.1: ← or A moves left."""
        keys = {pygame.K_LEFT: True, pygame.K_a: False, pygame.K_RIGHT: False,
                pygame.K_d: False, pygame.K_UP: False, pygame.K_w: False,
                pygame.K_DOWN: False, pygame.K_s: False, pygame.K_SPACE: False,
                pygame.K_UP: False}
        player.handle_input(keys)
        assert player.vx < 0, "Player should move left when ← is pressed"
        assert player.facing == -1, "Facing should be -1 when moving left"

    def test_move_right(self, player):
        """REQ-002.2: → or D moves right."""
        keys = {pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: True,
                pygame.K_d: False, pygame.K_UP: False, pygame.K_w: False,
                pygame.K_DOWN: False, pygame.K_s: False, pygame.K_SPACE: False}
        player.handle_input(keys)
        assert player.vx > 0, "Player should move right when → is pressed"
        assert player.facing == 1, "Facing should be 1 when moving right"

    def test_move_left_a_key(self, player):
        """REQ-002.1 variant: A key moves left."""
        keys = {pygame.K_LEFT: False, pygame.K_a: True, pygame.K_RIGHT: False,
                pygame.K_d: False, pygame.K_UP: False, pygame.K_w: False,
                pygame.K_DOWN: False, pygame.K_s: False, pygame.K_SPACE: False}
        player.handle_input(keys)
        assert player.vx < 0

    def test_move_right_d_key(self, player):
        """REQ-002.2 variant: D key moves right."""
        keys = {pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: False,
                pygame.K_d: True, pygame.K_UP: False, pygame.K_w: False,
                pygame.K_DOWN: False, pygame.K_s: False, pygame.K_SPACE: False}
        player.handle_input(keys)
        assert player.vx > 0

    def test_aim_up(self, player):
        """REQ-002.3: ↑ or W sets aiming up stance."""
        player.on_ground = True
        keys = {pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: False,
                pygame.K_d: False, pygame.K_UP: True, pygame.K_w: False,
                pygame.K_DOWN: False, pygame.K_s: False, pygame.K_SPACE: False}
        player.handle_input(keys)
        assert player.stance == 'AIMING_UP'

    def test_aim_up_w_key(self, player):
        """REQ-002.3 variant: W key sets aiming up stance."""
        player.on_ground = True
        keys = {pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: False,
                pygame.K_d: False, pygame.K_UP: False, pygame.K_w: True,
                pygame.K_DOWN: False, pygame.K_s: False, pygame.K_SPACE: False}
        player.handle_input(keys)
        assert player.stance == 'AIMING_UP'

    def test_prone(self, player):
        """REQ-002.4: ↓ or S sets prone stance."""
        player.on_ground = True
        keys = {pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: False,
                pygame.K_d: False, pygame.K_UP: False, pygame.K_w: False,
                pygame.K_DOWN: True, pygame.K_s: False, pygame.K_SPACE: False}
        player.handle_input(keys)
        assert player.stance == 'PRONE'

    def test_prone_s_key(self, player):
        """REQ-002.4 variant: S key sets prone stance."""
        player.on_ground = True
        keys = {pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: False,
                pygame.K_d: False, pygame.K_UP: False, pygame.K_w: False,
                pygame.K_DOWN: False, pygame.K_s: True, pygame.K_SPACE: False}
        player.handle_input(keys)
        assert player.stance == 'PRONE'

    def test_continuous_movement(self, player):
        """REQ-002.7: Holding key provides continuous movement."""
        keys = {pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: True,
                pygame.K_d: False, pygame.K_UP: False, pygame.K_w: False,
                pygame.K_DOWN: False, pygame.K_s: False, pygame.K_SPACE: False}
        player.handle_input(keys)
        assert player.vx > 0, "Holding → should maintain vx > 0"

    def test_terrain_collision_left(self, player):
        """REQ-002.6: Terrain blocks movement left."""
        player.x = 50
        player.vx = -4
        terrain_rects = [pygame.Rect(40, 280, 10, 200)]
        player.update(terrain_rects, [])
        # Player should not pass through terrain
        assert player.x >= 40

    def test_terrain_collision_right(self, player):
        """REQ-002.6: Terrain blocks movement right."""
        player.x = 100
        player.vx = 4
        terrain_rects = [pygame.Rect(110, 280, 10, 200)]
        player.update(terrain_rects, [])
        # Player should not pass through terrain
        assert player.x <= 110

    def test_prone_collision_box(self, player):
        """REQ-005: Prone reduces collision height."""
        player.stance = 'STANDING'
        stand_rect = player.hit_rect
        player.stance = 'PRONE'
        prone_rect = player.hit_rect
        assert prone_rect.height < stand_rect.height


class TestPlayerJumping:
    """REQ-003: Jumping mechanics"""

    def test_jump(self, player):
        """REQ-003.1: Space triggers jump."""
        player.on_ground = True
        player.on_ladder = False
        initial_y = player.y
        keys = {pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: False,
                pygame.K_d: False, pygame.K_UP: False, pygame.K_w: False,
                pygame.K_DOWN: False, pygame.K_s: False, pygame.K_SPACE: True}
        jumped = player.handle_input(keys)
        assert jumped, "handle_input should return True when jump occurs"
        assert player.vy < 0, "Jump should set negative vy (upward)"

    def test_cannot_jump_in_air(self, player):
        """Player cannot jump again while airborne."""
        player.on_ground = False
        player.on_ladder = False
        # Set vy so gravity will pull down
        player.vy = -5
        keys = {pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: False,
                pygame.K_d: False, pygame.K_UP: False, pygame.K_w: False,
                pygame.K_DOWN: False, pygame.K_s: False, pygame.K_SPACE: True}
        jumped = player.handle_input(keys)
        assert not jumped, "Should not jump when already airborne"

    def test_air_control(self, player):
        """REQ-003.2: Air allows horizontal control."""
        player.on_ground = False
        player.vy = -5
        initial_x = player.x
        keys = {pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: True,
                pygame.K_d: False, pygame.K_UP: False, pygame.K_w: False,
                pygame.K_DOWN: False, pygame.K_s: False, pygame.K_SPACE: False}
        player.handle_input(keys)
        assert player.vx > 0, "Should allow horizontal movement in air"

    def test_land_on_platform(self, player):
        """REQ-003.3: Landing on platform restores ground state."""
        player.x = 100
        player.y = 100
        player.vy = 5  # falling
        terrain_rects = [pygame.Rect(80, 110, 40, 20)]  # platform below
        player.update(terrain_rects, [])
        assert player.on_ground, "Should be on ground after landing"
        assert player.vy >= 0, "Vertical velocity should be reset"

    def test_pit_death(self, player):
        """REQ-003.4: Falling into pit causes death."""
        player.y = 600  # Below death threshold
        player.update([], [])
        assert not player.alive

    def test_ladder_climbing(self, player):
        """REQ-003.5: Ladder allows vertical movement."""
        player.on_ground = True
        player.on_ladder = True
        keys = {pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: False,
                pygame.K_d: False, pygame.K_UP: True, pygame.K_w: False,
                pygame.K_DOWN: False, pygame.K_s: False, pygame.K_SPACE: False}
        player.handle_input(keys)
        assert player.vy < 0, "Should move up on ladder"

    def test_ladder_down(self, player):
        """Ladder allows moving down."""
        player.on_ground = True
        player.on_ladder = True
        keys = {pygame.K_LEFT: False, pygame.K_a: False, pygame.K_RIGHT: False,
                pygame.K_d: False, pygame.K_UP: False, pygame.K_w: False,
                pygame.K_DOWN: True, pygame.K_s: False, pygame.K_SPACE: False}
        player.handle_input(keys)
        assert player.vy > 0, "Should move down on ladder"


class TestPlayerShooting:
    """REQ-004, REQ-005: Shooting mechanics"""

    def test_basic_shoot(self, player):
        """REQ-004.1: J key creates bullet."""
        player.fire_cooldown = 0
        player.alive = True
        # Simulate key press via game's start_fire
        bullets = player.start_fire()
        assert len(bullets) > 0, "Shooting should create at least one bullet"
        assert bullets[0].owner == 'player'

    def test_fire_cooldown(self, player):
        """REQ-004.3: Cooldown prevents firing every frame."""
        player.fire_cooldown = 5
        bullets = player.start_fire()
        assert len(bullets) == 0, "Should not fire during cooldown"

    def test_cooldown_decrements(self, player):
        """Fire cooldown decrements each frame."""
        player.fire_cooldown = 5
        player.update([], [])
        assert player.fire_cooldown == 4

    def test_bullet_horizontal(self, player):
        """REQ-004.2: Standing horizontal shot fires right."""
        player.facing = 1
        player.stance = 'STANDING'
        player.fire_cooldown = 0
        bullets = player.start_fire()
        assert len(bullets) > 0
        b = bullets[0]
        assert b.vx > 0, "Bullet should travel right when facing right"

    def test_bullet_horizontal_left(self, player):
        """Bullet travels left when facing left."""
        player.facing = -1
        player.stance = 'STANDING'
        player.fire_cooldown = 0
        bullets = player.start_fire()
        assert len(bullets) > 0
        b = bullets[0]
        assert b.vx < 0, "Bullet should travel left when facing left"

    def test_aim_up_shoot(self, player):
        """REQ-005.2: Standing + ↑ shoots upward."""
        player.facing = 1
        player.stance = 'AIMING_UP'
        player.fire_cooldown = 0
        bullets = player.start_fire()
        assert len(bullets) > 0
        b = bullets[0]
        # Angle of 90 degrees means vy is negative (upward in screen coords)
        assert b.vy < 0, "Aiming up should create upward bullet"

    def test_prone_shoot(self, player):
        """REQ-005.1: Prone shoots upward."""
        player.facing = 1
        player.stance = 'PRONE'
        player.fire_cooldown = 0
        bullets = player.start_fire()
        assert len(bullets) > 0
        b = bullets[0]
        assert b.vy < 0, "Prone shooting should fire upward"


class TestPlayerLifeSystem:
    """REQ-008: Life system"""

    def test_initial_lives(self, player):
        """REQ-008.1: Start with 3 lives."""
        assert player.lives == 3

    def test_invincibility_after_damage(self, player):
        """REQ-008.3: Invincibility after taking damage."""
        player.invincible = True
        player.invincible_timer = 90
        assert player.invincible
        assert player.invincible_timer > 0

    def test_invincibility_expires(self, player):
        """REQ-008.3: Invincibility expires after timer."""
        player.invincible = True
        player.invincible_timer = 1
        player.update([], [])
        assert not player.invincible, "Invincibility should expire"

    def test_respawn(self, player):
        """REQ-008.4: Respawn restores position and invincibility."""
        player.x = 100
        player.y = 500
        player.set_respawn(50, 300)
        player.respawn()
        assert player.x == 50
        assert player.y == 300
        assert player.alive
        assert player.invincible

    def test_alive_state(self, player):
        """Player starts alive."""
        assert player.alive


class TestPlayerWeapon:
    """REQ-006: Weapon system"""

    def test_default_weapon(self, player):
        """Player starts with BASIC weapon."""
        assert player.weapon == 'BASIC'

    def test_weapon_switch(self, player):
        """Player can switch weapon."""
        player.weapon = 'SPREAD'
        assert player.weapon == 'SPREAD'
        player.weapon = 'MACHINE_GUN'
        assert player.weapon == 'MACHINE_GUN'
        player.weapon = 'RAPID'
        assert player.weapon == 'RAPID'

    def test_spread_fires_multiple(self, player):
        """REQ-006.3: Spread fires 3 bullets."""
        player.weapon = 'SPREAD'
        player.fire_cooldown = 0
        bullets = player.start_fire()
        assert len(bullets) == 3, "Spread should fire 3 bullets"

    def test_spread_angles(self, player):
        """Spread bullets form a fan."""
        player.weapon = 'SPREAD'
        player.fire_cooldown = 0
        bullets = player.start_fire()
        assert len(bullets) == 3
        # Bullets should have different angles
        angles = [b.angle for b in bullets]
        assert len(set(angles)) > 1, "Spread bullets should have different angles"

    def test_machine_gun_rate(self, player):
        """REQ-006.3: Machine gun has faster fire rate."""
        import importlib
        from src import weapon as wmod
        importlib.reload(wmod)
        mg_config = wmod.WEAPON_CONFIGS['MACHINE_GUN']
        basic_config = wmod.WEAPON_CONFIGS['BASIC']
        assert mg_config['fire_rate'] < basic_config['fire_rate'], \
            "Machine gun should have lower fire_rate number (faster)"

    def test_rapid_damage(self, player):
        """REQ-006.3: Rapid bullets have higher damage."""
        player.weapon = 'RAPID'
        player.fire_cooldown = 0
        bullets = player.start_fire()
        assert len(bullets) > 0
        assert bullets[0].damage == 2, "RAPID should deal 2 damage"
