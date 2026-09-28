#!/usr/bin/env python3
"""Contra - Returns  魂斗罗 - 归来

A classic Contra-style side-scrolling shooter game built with Python + Pygame.
All assets are procedurally generated.
"""

import sys
import os

# Ensure the project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.game import Game


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
