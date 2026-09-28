"""UI screens — Title, Pause, Game Over, Stage Clear, Win."""

import pygame


def draw_title_screen(surf, screen_width=800, screen_height=600):
    """Draw the title screen."""
    # Background gradient
    for y in range(screen_height):
        r = int(10 + y * 0.02)
        g = int(10 + y * 0.03)
        b = int(20 + y * 0.04)
        surf.fill((min(r, 30), min(g, 40), min(b, 50)), (0, y, screen_width, 1))

    # Decorative lines
    for i in range(5):
        y = 180 + i * 60
        alpha = 30 + i * 20
        pygame.draw.line(surf, (alpha, alpha, alpha),
                         (0, y), (screen_width, y), 2)

    # Title shadow
    font_title = pygame.font.Font(None, 72)
    shadow = font_title.render("CONTRA - RETURNS", True, (100, 20, 20))
    title = font_title.render("CONTRA - RETURNS", True, (255, 50, 50))
    surf.blit(shadow, (screen_width // 2 - shadow.get_width() // 2 + 3, 143))
    surf.blit(title, (screen_width // 2 - title.get_width() // 2, 140))

    # Subtitle
    font_sub = pygame.font.Font(None, 28)
    subtitle = font_sub.render("魂斗罗 - 归来", True, (200, 200, 100))
    surf.blit(subtitle, (screen_width // 2 - subtitle.get_width() // 2, 220))

    # Instructions
    font_inst = pygame.font.Font(None, 24)
    lines = [
        "按 Enter 或 Space 开始游戏",
        "",
        "操作方法:",
        "← → / A D  移动     ↑ / W  仰角射击",
        "↓ / S  趴下            Space  跳跃",
        "J / Z  射击             P / Esc  暂停",
    ]
    y_off = 300
    for line in lines:
        if line == "":
            y_off += 10
            continue
        text = font_inst.render(line, True, (200, 200, 200))
        surf.blit(text, (screen_width // 2 - text.get_width() // 2, y_off))
        y_off += 30

    # Version
    font_v = pygame.font.Font(None, 16)
    ver = font_v.render("v1.0  |  程序化生成  |  Python + Pygame", True, (100, 100, 100))
    surf.blit(ver, (screen_width // 2 - ver.get_width() // 2, screen_height - 40))

    # Pixel decoration
    for x in range(0, screen_width, 20):
        for y in range(0, screen_height, 20):
            if (x // 20 + y // 20) % 7 == 0:
                c = (20, 30, 20) if (x // 20) % 2 == 0 else (30, 20, 20)
                surf.set_at((x, y), c)


def draw_pause_overlay(surf):
    """Draw pause overlay on top of the game."""
    # Semi-transparent overlay
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(160)
    overlay.fill((0, 0, 0))
    surf.blit(overlay, (0, 0))

    font_big = pygame.font.Font(None, 64)
    text = font_big.render("PAUSED", True, (255, 255, 255))
    surf.blit(text, (400 - text.get_width() // 2, 250))

    font_small = pygame.font.Font(None, 28)
    hint = font_small.render("按 P 或 Esc 继续", True, (200, 200, 200))
    surf.blit(hint, (400 - hint.get_width() // 2, 320))


def draw_game_over_screen(surf, score, screen_width=800, screen_height=600):
    """Draw Game Over screen."""
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(200)
    overlay.fill((20, 0, 0))
    surf.blit(overlay, (0, 0))

    font_big = pygame.font.Font(None, 64)
    text = font_big.render("GAME OVER", True, (255, 50, 50))
    surf.blit(text, (screen_width // 2 - text.get_width() // 2, 200))

    font_score = pygame.font.Font(None, 36)
    score_text = font_score.render(f"最终得分: {score}", True, (255, 255, 200))
    surf.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 280))

    font_hint = pygame.font.Font(None, 24)
    hint1 = font_hint.render("按 Enter 重新开始", True, (200, 200, 200))
    hint2 = font_hint.render("按 Esc 退出", True, (150, 150, 150))
    surf.blit(hint1, (screen_width // 2 - hint1.get_width() // 2, 350))
    surf.blit(hint2, (screen_width // 2 - hint2.get_width() // 2, 390))


def draw_stage_clear_screen(surf, stage, screen_width=800, screen_height=600):
    """Draw stage clear transition screen."""
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 20))
    surf.blit(overlay, (0, 0))

    font_big = pygame.font.Font(None, 56)
    text = font_big.render(f"STAGE {stage} CLEAR", True, (100, 255, 100))
    surf.blit(text, (screen_width // 2 - text.get_width() // 2, 260))

    font_hint = pygame.font.Font(None, 24)
    hint = font_hint.render("准备进入下一关...", True, (200, 200, 200))
    surf.blit(hint, (screen_width // 2 - hint.get_width() // 2, 330))


def draw_win_screen(surf, score, screen_width=800, screen_height=600):
    """Draw victory/win screen."""
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(200)
    overlay.fill((0, 10, 0))
    surf.blit(overlay, (0, 0))

    # Big congratulations
    font_big = pygame.font.Font(None, 56)
    text = font_big.render("CONGRATULATIONS!", True, (255, 255, 100))
    surf.blit(text, (screen_width // 2 - text.get_width() // 2, 180))

    font_sub = pygame.font.Font(None, 36)
    sub = font_sub.render("恭喜通关！", True, (255, 200, 100))
    surf.blit(sub, (screen_width // 2 - sub.get_width() // 2, 240))

    font_score = pygame.font.Font(None, 32)
    score_text = font_score.render(f"最终得分: {score}", True, (255, 255, 200))
    surf.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 300))

    font_hint = pygame.font.Font(None, 24)
    hint1 = font_hint.render("按 Enter 回到标题画面", True, (200, 200, 200))
    hint2 = font_hint.render("按 Esc 退出", True, (150, 150, 150))
    surf.blit(hint1, (screen_width // 2 - hint1.get_width() // 2, 370))
    surf.blit(hint2, (screen_width // 2 - hint2.get_width() // 2, 410))

    # Decorative particles
    import random
    for _ in range(30):
        fx = random.randint(0, screen_width)
        fy = random.randint(0, screen_height)
        fc = (random.randint(100, 255), random.randint(100, 255),
              random.randint(100, 255))
        surf.set_at((fx, fy), fc)
