from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from Funktions import allFunktions
from Einstellungen import Einstellungen

class Menu(Entity):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.functions = allFunktions()
        self.paused = False
        self.exit_button = None
        self.settings_button = None
        self.settings_panel = None
        self.background = None


    def show_fps(self):
        fps = int(1 / time.dt)
        print(f"FPS: {fps}")

    def remove(self):
        self.resume_button.disable()

        #self.ground = Entity(model='raum01.blend',collider='mesh',position=(0, -1, 0))

       # self.player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
    def unpause(self):
        self.paused = False
        application.paused = False
        self.exit_button.disable()
        self.exit_button = None
        self.settings_button.disable()
        self.settings_button = None
        if self.settings_panel:
            destroy(self.settings_panel)
            self.settings_panel = None
        destroy(self.background)
        self.background = None
        self.player.cursor.enabled = True
        mouse.locked = True
        self.remove()

    def toggle_settings(self):
        if self.settings_panel:
            destroy(self.settings_panel)
            self.settings_panel = None
            self.exit_button.enabled = True
            self.resume_button.enabled = True
            return


        self.exit_button.enabled = False
        self.resume_button.enabled = False

        self.settings_panel = Einstellungen()

    def input(self, key):
        if key == 'escape':
            if not self.paused:
                self.paused = True
                self.background = Entity(
                    parent=camera.ui,
                    model='quad',
                    scale=(camera.aspect_ratio, 1),
                    color=color.dark_gray,
                    z=1,
                )
                self.exit_button = self.functions.on_button_click(key)
                self.resume_button = self.functions.on_resume_button_click(self.unpause)
                self.settings_button = self.functions.on_settings_button_click(self.toggle_settings)
                self.player.cursor.enabled = False
                mouse.locked = False
                application.paused = True

