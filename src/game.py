"""Game main loop and state management."""

import random
import sys
import pygame

from src.player import Player
from src.camera import Camera
from src.hud import HUD
from src.ui import (
    draw_title_screen, draw_pause_overlay, draw_game_over_screen,
    draw_stage_clear_screen, draw_win_screen,
)
from src.level import Level
from src.bullet import Bullet
from src.enemy import PatrolEnemy, SentryEnemy
from assets.sounds import (
    make_shoot_sound, make_jump_sound, make_explosion_sound,
    make_pickup_sound, make_hit_sound, make_boss_hit_sound,
    make_stage_clear_sound, make_game_over_sound,
)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
LEVEL_FILES = ['level1.json', 'level2.json']

# States
STATE_TITLE = 'TITLE'
STATE_PLAYING = 'PLAYING'
STATE_PAUSED = 'PAUSED'
STATE_GAME_OVER = 'GAME_OVER'
STATE_STAGE_CLEAR = 'STAGE_CLEAR'
STATE_WIN = 'WIN'


class Game:
    """Main game controller."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=1)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Contra - Returns  魂斗罗 - 归来")
        self.clock = pygame.time.Clock()
        self.running = True

        # Pre-generate sounds
        self.sounds = {
            'shoot_basic': make_shoot_sound('BASIC'),
            'shoot_spread': make_shoot_sound('SPREAD'),
            'shoot_machine': make_shoot_sound('MACHINE_GUN'),
            'shoot_rapid': make_shoot_sound('RAPID'),
            'jump': make_jump_sound(),
            'explosion': make_explosion_sound(),
            'pickup': make_pickup_sound(),
            'hit': make_hit_sound(),
            'boss_hit': make_boss_hit_sound(),
            'stage_clear': make_stage_clear_sound(),
            'game_over': make_game_over_sound(),
        }

        # Game state
        self.state = STATE_TITLE
        self.score = 0
        self.current_level_idx = 0
        self.level = None
        self.player = None
        self.camera = None
        self.hud = HUD()
        self.bullets = []
        self.enemy_bullets = []
        self.stage_clear_timer = 0
        self.just_jumped = False

        self._init_level(0)

    def _init_level(self, level_idx):
        """Initialize or reset a level."""
        self.current_level_idx = level_idx
        if level_idx >= len(LEVEL_FILES):
            self.state = STATE_WIN
            return

        self.level = Level(LEVEL_FILES[level_idx])

        spawn = self.level.player_spawn
        if self.player is None:
            self.player = Player(spawn[0], spawn[1])
            self.player.set_respawn(spawn[0], spawn[1])
        else:
            self.player.x = spawn[0]
            self.player.y = spawn[1]
            self.player.vx = 0
            self.player.vy = 0
            self.player.alive = True
            self.player.on_ground = False
            self.player.stance = 'STANDING'
            self.player.set_respawn(spawn[0], spawn[1])

        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT,
                             self.level.level_width)
        self.bullets = []
        self.enemy_bullets = []
        self.just_jumped = False

    def _next_level(self):
        """Advance to the next level or show win screen."""
        if self.current_level_idx + 1 >= len(LEVEL_FILES):
            self.state = STATE_WIN
            self.sounds['stage_clear'].play()
        else:
            self._init_level(self.current_level_idx + 1)
            self.state = STATE_PLAYING

    def _reset_game(self):
        """Full game reset back to level 1."""
        self.score = 0
        self.player = None
        self.current_level_idx = 0
        self._init_level(0)
        self.state = STATE_TITLE

    def handle_events(self):
        """Process input events."""
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                # Global: Escape quits anywhere
                if event.key == pygame.K_ESCAPE:
                    if self.state == STATE_PLAYING:
                        self.state = STATE_PAUSED
                    elif self.state == STATE_PAUSED:
                        self.state = STATE_PLAYING
                    elif self.state in (STATE_GAME_OVER, STATE_WIN, STATE_TITLE):
                        self.running = False
                    continue

                if self.state == STATE_TITLE:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.state = STATE_PLAYING
                        self._init_level(0)
                    continue

                if self.state == STATE_PLAYING:
                    if event.key == pygame.K_p:
                        self.state = STATE_PAUSED
                        continue
                    if event.key in (pygame.K_j, pygame.K_z):
                        bullets = self.player.start_fire()
                        for b in bullets:
                            self.bullets.append(b)
                        if bullets:
                            self._play_shoot_sound()
                    continue

                if self.state == STATE_PAUSED:
                    if event.key == pygame.K_p:
                        self.state = STATE_PLAYING
                    continue

                if self.state == STATE_GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        self._reset_game()
                    continue

                if self.state == STATE_WIN:
                    if event.key == pygame.K_RETURN:
                        self._reset_game()
                    continue

                if self.state == STATE_STAGE_CLEAR:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self._next_level()
                    continue

        # Continuous key handling for PLAYING state
        if self.state == STATE_PLAYING:
            if self.player and self.player.alive:
                jumped = self.player.handle_input(keys)
                if jumped and not self.just_jumped:
                    self.sounds['jump'].play()
                self.just_jumped = jumped

                # Continuous fire when holding J/Z
                if keys[pygame.K_j] or keys[pygame.K_z]:
                    bullets = self.player.start_fire()
                    for b in bullets:
                        self.bullets.append(b)
                    if bullets:
                        self._play_shoot_sound()

    def _play_shoot_sound(self):
        """Play the appropriate shooting sound."""
        w = self.player.weapon
        if w == 'SPREAD':
            self.sounds['shoot_spread'].play()
        elif w == 'MACHINE_GUN':
            self.sounds['shoot_machine'].play()
        elif w == 'RAPID':
            self.sounds['shoot_rapid'].play()
        else:
            self.sounds['shoot_basic'].play()

    def update(self):
        """Update game logic."""
        if self.state == STATE_STAGE_CLEAR:
            self.stage_clear_timer -= 1
            if self.stage_clear_timer <= 0:
                self._next_level()
            return
        
        if self.state != STATE_PLAYING:
            return

        # Player update
        if self.player and self.player.alive:
            self.player.update(
                self.level.terrain_rects, self.level.ladder_rects)

            # Check pit death
            if not self.player.alive:
                self._player_died()
                return

        # Camera
        if self.player:
            self.camera.update(self.player.x, self.player.y)

        # Update bullets
        for b in self.bullets[:]:
            b.update()
            if (b.x < self.camera.x - 50 or
                b.x > self.camera.x + SCREEN_WIDTH + 50 or
                b.y < -50 or b.y > SCREEN_HEIGHT + 50):
                self.bullets.remove(b)
                continue
            # Check terrain collision
            for rect in self.level.terrain_rects:
                if b.rect.colliderect(rect):
                    if b in self.bullets:
                        self.bullets.remove(b)
                    break

        # Update enemy bullets
        for b in self.enemy_bullets[:]:
            b.update()
            if (b.x < self.camera.x - 50 or
                b.x > self.camera.x + SCREEN_WIDTH + 50 or
                b.y < -50 or b.y > SCREEN_HEIGHT + 50):
                self.enemy_bullets.remove(b)
                continue
            # Check terrain collision
            for rect in self.level.terrain_rects:
                if b.rect.colliderect(rect):
                    if b in self.enemy_bullets:
                        self.enemy_bullets.remove(b)
                    break

        # Update enemies
        for enemy in self.level.enemies[:]:
            if isinstance(enemy, PatrolEnemy):
                remove = enemy.update(self.level.terrain_rects)
                if remove:
                    self.level.enemies.remove(enemy)
            elif isinstance(enemy, SentryEnemy):
                if self.player:
                    px = self.player.x
                    py = self.player.y
                else:
                    px, py = 0, 0
                remove, bullet = enemy.update(
                    self.level.terrain_rects, px, py, 1.0 / FPS)
                if bullet:
                    self.enemy_bullets.append(bullet)
                if remove:
                    self.level.enemies.remove(enemy)

        # Update items
        for item in self.level.items[:]:
            item.update()
            if item.collected:
                self.level.items.remove(item)

        # Update boss
        if self.level.boss:
            px = self.player.x if self.player else 0
            py = self.player.y if self.player else 0
            boss_done, boss_bullets, summon = self.level.boss.update(
                1.0 / FPS, px, py)
            for b in boss_bullets:
                self.enemy_bullets.append(b)
            if summon:
                for s in summon:
                    ex = self.level.boss.x + random.randint(-60, 60)
                    ey = self.level.boss.y - 20
                    pr = [ex - 60, ex + 60]
                    self.level.enemies.append(PatrolEnemy(ex, ey, pr))

            if not self.level.boss.alive and boss_done:
                # Boss defeated!
                self.score += 5000
                self.sounds['stage_clear'].play()
                self.state = STATE_STAGE_CLEAR
                self.stage_clear_timer = 180  # 3 seconds
                return

        # Check boss activation
        if (self.level.boss and not self.level.boss.active and
                self.player and
                self.player.x >= self.level.get_boss_trigger_x()):
            self.level.activate_boss()

        # Bullet-enemy collision
        for bullet in self.bullets[:]:
            if not bullet.alive:
                continue
            # Check vs enemies
            for enemy in self.level.enemies[:]:
                if not enemy.alive:
                    continue
                if bullet.rect.colliderect(enemy.rect):
                    killed = enemy.take_damage()
                    if killed:
                        self.score += 100
                        self.sounds['explosion'].play()
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break

            # Check vs boss
            if self.level.boss and self.level.boss.alive and self.level.boss.active:
                if bullet.rect.colliderect(self.level.boss.rect):
                    defeated = self.level.boss.take_damage(bullet.damage)
                    self.sounds['boss_hit'].play()
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

        # Enemy bullet vs player
        if self.player and self.player.alive:
            for bullet in self.enemy_bullets[:]:
                if self.player.hit_rect.colliderect(bullet.rect):
                    if bullet in self.enemy_bullets:
                        self.enemy_bullets.remove(bullet)
                    if not self.player.invincible:
                        self._player_died()
                        return

            # Enemy body vs player
            for enemy in self.level.enemies:
                if enemy.alive and self.player.alive:
                    if (self.player.hit_rect.colliderect(enemy.rect) and
                            not self.player.invincible):
                        self._player_died()
                        return

            # Boss body vs player
            if (self.level.boss and self.level.boss.alive and
                    self.level.boss.active and self.player.alive):
                if (self.player.hit_rect.colliderect(self.level.boss.rect) and
                        not self.player.invincible):
                    self._player_died()
                    return

        # Item collection
        if self.player and self.player.alive:
            for item in self.level.items[:]:
                if not item.collected and self.player.rect.colliderect(item.rect):
                    item.collected = True
                    self.sounds['pickup'].play()
                    if item.weapon_type:
                        self.player.weapon = item.weapon_type
                    if item.is_1up:
                        self.player.lives = min(9, self.player.lives + 1)
                    if item.score_value > 0:
                        self.score += item.score_value

    def _player_died(self):
        """Handle player death."""
        self.sounds['hit'].play()
        self.player.lives -= 1
        if self.player.lives <= 0:
            self.sounds['game_over'].play()
            self.state = STATE_GAME_OVER
        else:
            # Respawn at checkpoint
            self.player.respawn()
            # Reset enemy bullets
            self.enemy_bullets = []

    def draw(self):
        """Render the current frame."""
        self.screen.fill((0, 0, 0))

        if self.state == STATE_TITLE:
            draw_title_screen(self.screen)
            pygame.display.flip()
            return

        if self.state in (STATE_GAME_OVER, STATE_WIN):
            # Draw last frame background
            if self.level:
                self.level.draw_background(self.screen, self.camera.x if self.camera else 0)
            if self.state == STATE_GAME_OVER:
                draw_game_over_screen(self.screen, self.score)
            else:
                draw_win_screen(self.screen, self.score)
            pygame.display.flip()
            return

        if self.state == STATE_STAGE_CLEAR:
            # Draw level then overlay
            if self.level:
                self._draw_game()
            draw_stage_clear_screen(self.screen, self.current_level_idx + 1)
            pygame.display.flip()
            return

        # PLAYING or PAUSED
        self._draw_game()

        if self.state == STATE_PAUSED:
            draw_pause_overlay(self.screen)

        pygame.display.flip()

    def _draw_game(self):
        """Draw the game world."""
        if not self.level or not self.camera:
            return

        camera_x = self.camera.x

        # Background
        self.level.draw_background(self.screen, camera_x)

        # Terrain
        self.level.draw_terrain(self.screen, camera_x)

        # Items
        for item in self.level.items:
            item.draw(self.screen, camera_x)

        # Enemies
        for enemy in self.level.enemies:
            enemy.draw(self.screen, camera_x)

        # Boss
        if self.level.boss:
            self.level.boss.draw(self.screen, camera_x)

        # Bullets
        for bullet in self.bullets:
            bullet.draw(self.screen, camera_x)
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen, camera_x)

        # Player
        if self.player:
            self.player.draw(self.screen, camera_x)

        # HUD
        if self.player:
            self.hud.draw(self.screen, self.player.lives, self.score,
                          self.player.weapon, self.current_level_idx + 1,
                          self.level.boss if self.level else None)

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
