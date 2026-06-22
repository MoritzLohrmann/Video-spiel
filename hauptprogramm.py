from ursina import *
from menu import *


def start():
    app = Ursina(title="3d", borderless=False)
    menu = Menu()
    ground = Entity(model='raum01.blend',collider='mesh',position=(0, -1, 0))
    player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
    app.run()