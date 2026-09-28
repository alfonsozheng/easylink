"""Heads-Up Display rendering."""

import pygame


class HUD:
    """Game HUD showing lives, score, weapon, level info, and boss HP bar."""

    def __init__(self):
        self.font_large = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)

    def draw(self, surf, lives, score, weapon, level, boss=None):
        """Draw HUD elements."""
        # Background bar
        pygame.draw.rect(surf, (0, 0, 0, 180), (0, 0, 800, 32))
        pygame.draw.rect(surf, (30, 30, 30), (0, 0, 800, 32))
        pygame.draw.line(surf, (100, 100, 100), (0, 32), (800, 32), 1)

        # Lives
        heart = self.font_small.render(f"❤", True, (255, 50, 50))
        lives_text = self.font_small.render(f"× {lives}", True, (255, 255, 255))
        surf.blit(heart, (10, 6))
        surf.blit(lives_text, (30, 6))

        # Level
        level_text = self.font_small.render(f"STAGE {level}", True, (200, 200, 100))
        surf.blit(level_text, (300, 6))

        # Weapon
        weapon_names = {
            'BASIC': 'BASIC', 'SPREAD': 'SPREAD S',
            'MACHINE_GUN': 'MACHINE M', 'RAPID': 'RAPID R',
        }
        wname = weapon_names.get(weapon, weapon)
        w_text = self.font_small.render(wname, True, (100, 200, 255))
        surf.blit(w_text, (480, 6))

        # Score
        score_text = self.font_small.render(f"SCORE: {score}", True, (255, 255, 200))
        surf.blit(score_text, (630, 6))

        # Boss HP bar (if boss is active and alive)
        if boss and boss.active and boss.alive:
            bar_y = 40
            bar_width = 300
            bar_height = 10
            bar_x = (800 - bar_width) // 2

            # Background
            pygame.draw.rect(surf, (60, 20, 20), (bar_x, bar_y, bar_width, bar_height))
            # HP fill
            if boss.max_hp > 0:
                ratio = boss.hp / boss.max_hp
                fill_w = int(bar_width * ratio)
                hp_color = (50, 200, 50) if ratio > 0.5 else \
                           (200, 200, 50) if ratio > 0.25 else (200, 50, 50)
                pygame.draw.rect(surf, hp_color, (bar_x, bar_y, fill_w, bar_height))
            # Border
            pygame.draw.rect(surf, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 1)
            # Label
            boss_label = self.font_tiny.render("BOSS", True, (255, 255, 255))
            surf.blit(boss_label, (bar_x - 40, bar_y - 1))
