from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from Funktions import allFunktions

class Menu(Entity):
    def __init__(self):
        super().__init__()
        Button.default_color = color.red
        #self.b = Button(
        #    model='quad',
        #    scale=.05,
        #    x=-.5,
       #     color=color.lime,
        #    text='Start game',
        #    text_size=.5,
        #    text_color=color.black,
        #    on_click=self.remove
        #)
        self.functions = allFunktions()
        self.paused = False
        self.exit_button = None
        

    def show_fps(self):
        fps = int(1 / time.dt)
        print(f"FPS: {fps}")

    def remove(self):
        self.b.disable()

        #self.ground = Entity(model='raum01.blend',collider='mesh',position=(0, -1, 0))

       # self.player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
    def unpause(self):
        self.paused = False
        application.paused = False
        self.exit_button.disable()
        self.exit_button = None
        mouse.locked = True
        self.remove()
    

    def input(self, key):
        if key == 'escape':
            if not self.paused:
                self.paused = True
                self.exit_button = self.functions.on_button_click(key)
                self.b = Button(
                    model='quad',
                    scale=.05,
                    x=-.5,
                    color=color.lime,
                   text='Start game',
                   text_size=.5,
                   text_color=color.black,
                   on_click=self.unpause
                )
                mouse.locked = False
                application.paused = True

