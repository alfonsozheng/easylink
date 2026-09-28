"""Scroll camera following the player."""

import pygame


class Camera:
    """Horizontal scrolling camera that follows the player.

    The camera keeps the player at roughly 1/3 from the left and
    never scrolls backward (left).
    """

    def __init__(self, width, height, level_width):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.level_width = level_width
        self.target_x = 0

    def update(self, player_x, player_y):
        # Target: player at 1/3 screen width
        self.target_x = player_x - self.width // 3

        # Smooth follow
        diff = self.target_x - self.x
        self.x += diff * 0.1

        # Never scroll backward
        if self.x < 0:
            self.x = 0

        # Clamp to level boundaries
        max_x = self.level_width - self.width
        if self.x > max_x:
            self.x = max_x

        # Vertical follow
        self.y = player_y - self.height // 2
        if self.y < 0:
            self.y = 0
        max_y = 600 - self.height
        if self.y > max_y:
            self.y = max_y

    def apply(self, rect):
        return rect.move(-self.x, -self.y)

    def world_to_screen(self, world_x, world_y):
        return (world_x - self.x, world_y - self.y)
