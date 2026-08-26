from ursina import *

from Funktions import allFunktions
from Einstellungen import Einstellungen


class StartScreen(Entity):
    def __init__(self, on_start):
        super().__init__(parent=camera.ui)
        self.functions = allFunktions()
        self.settings_panel = None

        self.title = Text(
            parent=self,
            text='3D Shooter',
            y=.35,
            origin=(0, 0),
            scale=3,
            color=color.white,
        )

        self.play_button = self.functions.on_play_button_click(self.start_game)
        self.play_button.parent = self
        self.on_start = on_start

        self.gamemode_button = self.functions.on_gamemode_button_click(Func(print, 'Spielmodi: noch nicht verfügbar'))
        self.gamemode_button.parent = self

        self.settings_button = self.functions.on_settings_button_click(self.toggle_settings)
        self.settings_button.parent = self

    def start_game(self):
        self.disable()
        self.on_start()

    def toggle_settings(self):
        if self.settings_panel:
            destroy(self.settings_panel)
            self.settings_panel = None
            self.play_button.enabled = True
            self.gamemode_button.enabled = True
            return

        self.play_button.enabled = False
        self.gamemode_button.enabled = False

        self.settings_panel = Einstellungen()
