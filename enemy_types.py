from dataclasses import dataclass

from ursina import color


@dataclass
class EnemyType:
    name: str
    model: str  # bleibt erstmal 'cube', später kommt hier das GLB-Modell rein
    color: object
    scale: tuple
    max_hp: int
    speed: float
    attack_damage: int
    attack_rate: float  # Sekunden zwischen zwei Angriffen
    attack_range: float
    sight_range: float


# Neue Gegnertypen entstehen nur durch einen neuen Eintrag hier, enemy.py bleibt unverändert.
ENEMY_TYPES = {
    'basic': EnemyType(
        name='basic',
        model='cube',
        color=color.light_gray,
        scale=(1, 2, 1),
        max_hp=100,
        speed=5,
        attack_damage=10,
        attack_rate=1.0,
        attack_range=2,
        sight_range=40,
    ),
    'fast': EnemyType(
        name='fast',
        model='cube',
        color=color.yellow,
        scale=(.7, 1.4, .7),
        max_hp=50,
        speed=7,  # bewusst unter dem Spieler (8), damit man noch weglaufen kann
        attack_damage=5,
        attack_rate=.7,
        attack_range=2,
        sight_range=40,
    ),
    'tank': EnemyType(
        name='tank',
        model='cube',
        color=color.violet,
        scale=(1.6, 3, 1.6),
        max_hp=300,
        speed=3,
        attack_damage=25,
        attack_rate=1.5,
        attack_range=3,  # größerer Körper, sonst steckt er beim Angriff im Spieler
        sight_range=40,
    ),
}
