"""Procedural sound effect generation using Pygame mixer.

All sounds are generated programmatically via waveform synthesis.
No external audio files are required.
"""

import math
import struct
import io
import pygame

SAMPLE_RATE = 22050


def _make_wave(freq, duration, volume=0.5, wave_type='square',
               decay=True, noise=False):
    """Generate a waveform and return a pygame Sound object."""
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE

        if noise:
            import random
            val = random.uniform(-1, 1)
        elif wave_type == 'square':
            val = 1.0 if (t * freq) % 1.0 < 0.5 else -1.0
        elif wave_type == 'saw':
            val = 2.0 * ((t * freq) % 1.0) - 1.0
        elif wave_type == 'triangle':
            phase = (t * freq) % 1.0
            val = 4.0 * abs(phase - 0.5) - 1.0
        else:  # sine
            val = math.sin(2 * math.pi * freq * t)

        # Apply decay envelope
        if decay:
            env = 1.0 - (i / n_samples)
        else:
            env = 1.0

        # Mix
        val = max(-1.0, min(1.0, val * env * volume))
        samples.append(int(val * 32767 * 0.7))

    # Convert to 16-bit mono PCM
    buf = io.BytesIO()
    for s in samples:
        buf.write(struct.pack('<h', max(-32768, min(32767, s))))
    buf.seek(0)
    sound = pygame.mixer.Sound(buffer=buf.read())
    buf.close()
    return sound


def make_shoot_sound(weapon_type='BASIC'):
    """Shooting sound effect."""
    if weapon_type == 'MACHINE_GUN':
        return _make_wave(800, 0.08, volume=0.3, wave_type='square', decay=True)
    elif weapon_type == 'SPREAD':
        return _make_wave(300, 0.15, volume=0.4, wave_type='saw', decay=True)
    elif weapon_type == 'RAPID':
        return _make_wave(600, 0.10, volume=0.4, wave_type='triangle', decay=True)
    else:
        return _make_wave(500, 0.10, volume=0.3, wave_type='square', decay=True)


def make_jump_sound():
    """Jump sound effect - rising tone."""
    n_samples = int(SAMPLE_RATE * 0.15)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 200 + (t / 0.15) * 400  # rising
        val = math.sin(2 * math.pi * freq * t)
        env = 1.0 - (i / n_samples)
        val = max(-1.0, min(1.0, val * env * 0.4))
        samples.append(int(val * 32767))
    buf = io.BytesIO()
    for s in samples:
        buf.write(struct.pack('<h', max(-32768, min(32767, s))))
    buf.seek(0)
    sound = pygame.mixer.Sound(buffer=buf.read())
    buf.close()
    return sound


def make_explosion_sound():
    """Explosion sound - noise burst with decay."""
    return _make_wave(100, 0.3, volume=0.5, wave_type='square',
                      decay=True, noise=True)


def make_pickup_sound():
    """Item pickup - two-tone chime."""
    n_samples = int(SAMPLE_RATE * 0.2)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 600 if t < 0.1 else 900
        val = math.sin(2 * math.pi * freq * t)
        env = 1.0 - (i / n_samples)
        val = max(-1.0, min(1.0, val * env * 0.4))
        samples.append(int(val * 32767))
    buf = io.BytesIO()
    for s in samples:
        buf.write(struct.pack('<h', max(-32768, min(32767, s))))
    buf.seek(0)
    sound = pygame.mixer.Sound(buffer=buf.read())
    buf.close()
    return sound


def make_hit_sound():
    """Player hit sound."""
    return _make_wave(150, 0.25, volume=0.5, wave_type='saw', decay=True)


def make_boss_hit_sound():
    """Boss hit sound - deeper thud."""
    return _make_wave(80, 0.2, volume=0.6, wave_type='square', decay=True)


def make_stage_clear_sound():
    """Stage clear jingle."""
    n_samples = int(SAMPLE_RATE * 1.0)
    notes = [523, 659, 784, 1047]  # C5, E5, G5, C6
    samples = []
    note_len = n_samples // len(notes)
    for ni, freq in enumerate(notes):
        for i in range(note_len):
            t = i / SAMPLE_RATE
            val = math.sin(2 * math.pi * freq * t)
            env = 1.0 - (i / note_len) * 0.5
            val = max(-1.0, min(1.0, val * env * 0.4))
            samples.append(int(val * 32767))
    buf = io.BytesIO()
    for s in samples:
        buf.write(struct.pack('<h', max(-32768, min(32767, s))))
    buf.seek(0)
    sound = pygame.mixer.Sound(buffer=buf.read())
    buf.close()
    return sound


def make_game_over_sound():
    """Game over sound."""
    n_samples = int(SAMPLE_RATE * 0.8)
    notes = [392, 349, 330, 262]  # G4, F4, E4, C4
    samples = []
    note_len = n_samples // len(notes)
    for ni, freq in enumerate(notes):
        for i in range(note_len):
            t = i / SAMPLE_RATE
            val = math.sin(2 * math.pi * freq * t)
            env = 1.0 - (i / note_len) * 0.3
            val = max(-1.0, min(1.0, val * env * 0.4))
            samples.append(int(val * 32767))
    buf = io.BytesIO()
    for s in samples:
        buf.write(struct.pack('<h', max(-32768, min(32767, s))))
    buf.seek(0)
    sound = pygame.mixer.Sound(buffer=buf.read())
    buf.close()
    return sound
