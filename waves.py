from dataclasses import dataclass
import math


@dataclass
class WaveConfig:
    enemies: dict  # typ_name -> anzahl, die Namen kommen aus ENEMY_TYPES
    spawn_interval: float  # Sekunden zwischen zwei Spawns
    max_alive: int  # mehr Gegner gleichzeitig werden nicht gespawnt
    hp_multiplier: float = 1.0


# Neue Wellen entstehen nur durch einen neuen Eintrag hier
WAVES = [
    WaveConfig(enemies={'basic': 3}, spawn_interval=2.0, max_alive=3),
    WaveConfig(enemies={'basic': 4, 'fast': 2}, spawn_interval=1.8, max_alive=4),
    WaveConfig(enemies={'basic': 5, 'fast': 4}, spawn_interval=1.5, max_alive=5),
    WaveConfig(enemies={'basic': 5, 'fast': 4, 'tank': 1}, spawn_interval=1.5, max_alive=6),
    WaveConfig(enemies={'basic': 6, 'fast': 6, 'tank': 2}, spawn_interval=1.2, max_alive=8, hp_multiplier=1.2),
]

MAX_ALIVE_LIMIT = 20


def get_wave(number):
    # Die Zählung beginnt bei Welle 1
    if number <= len(WAVES):
        return WAVES[number - 1]

    # Endlose Wellen bauen auf der letzten Welle auf, extra = number - len(WAVES):
    #   anzahl pro typ = aufrunden(basis * (1 + 0.2 * extra))
    #   hp_multiplier  = basis + 0.15 * extra
    #   max_alive      = basis + extra, höchstens MAX_ALIVE_LIMIT
    # Das Limit schützt die Framerate, weil jeder Gegner pro Frame einen Raycast macht.
    last_wave = WAVES[-1]
    extra = number - len(WAVES)

    enemies = {}
    for type_name, count in last_wave.enemies.items():
        enemies[type_name] = math.ceil(count * (1 + .2 * extra))

    return WaveConfig(
        enemies=enemies,
        spawn_interval=last_wave.spawn_interval,
        max_alive=min(last_wave.max_alive + extra, MAX_ALIVE_LIMIT),
        hp_multiplier=last_wave.hp_multiplier + .15 * extra,
    )
