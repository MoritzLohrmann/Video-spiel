from ursina import *
from menu import *
from player import *
from gun import Gun
from enemy import Enemy

def start():
    app = Ursina(title="3d", borderless=False)
    menu = Menu()
    room = Entity(model='raum01.blend',collider='mesh',position=(0, -1, 0))
    #player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
    player = Player(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
    #waffentest kommst später in den player
    player.gun = None
    gun = Gun(player=player, parent=scene, position=(3, 0, 3), damage=15, fire_rate=0.25, magazine_size=8)
    gun.on_click = lambda: player.pickupGun(gun)
    enemy= Enemy(player=player, position=(0, 0, 5))

    app.run()