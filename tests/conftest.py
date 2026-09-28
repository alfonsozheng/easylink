"""Test fixtures and configuration for Contra game tests."""

import os
import sys
import pytest

# Set headless mode BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame

# Ensure project root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.player import Player
from src.camera import Camera
from src.hud import HUD
from src.level import Level
from src.bullet import Bullet
from src.enemy import PatrolEnemy, SentryEnemy
from src.boss import Boss
from src.item import Item
from src.game import Game


@pytest.fixture(scope='session', autouse=True)
def pygame_init():
    """Initialize pygame once for all tests."""
    pygame.init()
    pygame.display.set_mode((800, 600), pygame.HIDDEN)
    pygame.mixer.init(frequency=22050, size=-16, channels=1)
    yield
    pygame.quit()


@pytest.fixture
def dummy_screen():
    """Get a screen surface for drawing tests."""
    return pygame.Surface((800, 600))


@pytest.fixture
def player():
    """Create a player at default position."""
    return Player(200, 300)


@pytest.fixture
def camera():
    """Create a camera instance."""
    return Camera(800, 600, 6400)


@pytest.fixture
def level1():
    """Load level 1."""
    return Level('level1.json')


@pytest.fixture
def level2():
    """Load level 2."""
    return Level('level2.json')


@pytest.fixture
def hud():
    """Create HUD instance."""
    return HUD()


@pytest.fixture
def game():
    """Create game instance with headless pygame."""
    g = Game()
    # Ensure title state
    g.state = 'TITLE'
    return g


@pytest.fixture
def basic_bullet():
    """Create a basic player bullet."""
    return Bullet(200, 300, 0, 10, owner='player', weapon_type='BASIC', damage=1)


@pytest.fixture
def patrol_enemy():
    """Create a patrol enemy."""
    return PatrolEnemy(500, 400, [400, 600])


@pytest.fixture
def sentry_enemy():
    """Create a sentry enemy."""
    return SentryEnemy(700, 400, shoot_interval=1.5)


@pytest.fixture
def jungle_boss():
    """Create jungle boss."""
    return Boss({
        'type': 'jungle_boss',
        'x': 4600,
        'y': 360,
        'hp': 20,
        'attack_pattern': 'spread_shot'
    })


@pytest.fixture
def base_boss():
    """Create base boss."""
    return Boss({
        'type': 'base_boss',
        'x': 5800,
        'y': 340,
        'hp': 30,
        'attack_pattern': 'spread_shot_and_summon'
    })


@pytest.fixture
def item_weapon_s():
    """Create a weapon_S item."""
    return Item('weapon_S', 500, 300)


@pytest.fixture
def item_1up():
    """Create a 1UP item."""
    return Item('1UP', 600, 300)


@pytest.fixture
def item_score():
    """Create a score item."""
    return Item('score', 700, 300)
