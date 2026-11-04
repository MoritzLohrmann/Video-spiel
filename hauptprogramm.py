from ursina import *
from menu import *
from start_screen import StartScreen
from player import *
from gun import Gun
from spawner import EnemySpawner

def start():
    app = Ursina(title="3d", borderless=False)

    def load_game():
        room = Entity(model='Raum01.blend',collider='mesh',position=(0, -1, 0))
        #player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
        player = Player(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
        # Platzhalter für Raum01: Positionen hier anpassen, F3 zeigt sie im Spiel an.
        # Später liefert der Map-Generator die Punkte über spawner.add_spawn_points().
        spawn_points = [
            (-28, 0, 12), (-24, 0, -12), (-20, 0, -24), (12, 0, -28),
            (28, 0, -12), (24, 0, 12), (12, 0, 28), (-12, 0, 20),
        ]
        spawner = EnemySpawner(player=player, spawn_points=spawn_points)
        player.on_respawn = spawner.restart_wave
        menu = Menu(player, spawner)
        #waffentest kommst später in den player
        player.gun = None
        gun = Gun(player=player, parent=scene, position=(3, 0, 3), damage=15, fire_rate=0.25, magazine_size=8, model='revolver.blend',scale=(.2, .2, .2),
                  muzzle_offset=Vec3(0, 2.19, 1.95))  
        gun.on_click = lambda: player.pickupGun(gun)

    start_screen = StartScreen(on_start=load_game)

    app.run()