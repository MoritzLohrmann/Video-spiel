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
                scale=(.22, .09),
                color=color.hex('#dc2626'),
                highlight_color=color.hex('#ef4444'),
                pressed_color=color.hex('#b91c1c'),
                highlight_scale=1.05,
                text='Exit',
                text_size=1.3,
                text_color=color.white,
                on_click=self.exit_game
            )

    def exit_game(self):
        application.quit()