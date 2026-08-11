from ursina import *

class allFunktions:
    def __init__(self):
        pass

    def show_fps(self):
        fps = int(1 / time.dt)
        print(f"FPS: {fps}")

    def on_button_click(self, key):
        if key == 'escape':
            
            return Button(
                model='quad',
                scale=.05,
                x=.7,
                y=.4,
                color=color.lime,
                text='Exit',
                text_size=.5,
                text_color=color.black,
                on_click=self.exit_game
            )

    def exit_game(self):
        application.quit()