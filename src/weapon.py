"""Weapon system configuration."""

import pygame

WEAPON_CONFIGS = {
    'BASIC': {
        'name': '普通枪',
        'bullet_speed': 10,
        'fire_rate': 8,       # frames between shots
        'spread_count': 1,
        'spread_angle': 0,
        'damage': 1,
        'color': (255, 255, 200),
    },
    'SPREAD': {
        'name': '散弹枪 S',
        'bullet_speed': 8,
        'fire_rate': 12,
        'spread_count': 3,
        'spread_angle': 15,   # degrees
        'damage': 1,
        'color': (255, 200, 100),
    },
    'MACHINE_GUN': {
        'name': '机枪 M',
        'bullet_speed': 12,
        'fire_rate': 3,
        'spread_count': 1,
        'spread_angle': 0,
        'damage': 1,
        'color': (255, 255, 100),
    },
    'RAPID': {
        'name': '加速弹 R',
        'bullet_speed': 10,
        'fire_rate': 5,
        'spread_count': 1,
        'spread_angle': 0,
        'damage': 2,
        'color': (255, 150, 50),
    },
}

WEAPON_ORDER = ['BASIC', 'SPREAD', 'MACHINE_GUN', 'RAPID']
