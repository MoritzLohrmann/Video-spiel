from dataclasses import dataclass
import math


@dataclass
class WaveConfig:
    enemies: dict  
    spawn_interval: float  
    max_alive: int  
    hp_multiplier: float = 1.0



WAVES = [
    WaveConfig(enemies={'basic': 3}, spawn_interval=2.0, max_alive=3),
    WaveConfig(enemies={'basic': 4, 'fast': 2}, spawn_interval=1.8, max_alive=4),
    WaveConfig(enemies={'basic': 5, 'fast': 4}, spawn_interval=1.5, max_alive=5),
    WaveConfig(enemies={'basic': 5, 'fast': 4, 'tank': 1}, spawn_interval=1.5, max_alive=6),
    WaveConfig(enemies={'basic': 6, 'fast': 6, 'tank': 2}, spawn_interval=1.2, max_alive=8, hp_multiplier=1.2),
]

MAX_ALIVE_LIMIT = 20


def get_wave(number):
    
    if number <= len(WAVES):
        return WAVES[number - 1]

 
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
