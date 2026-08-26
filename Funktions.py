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


    #Fortsetzen Button(Pause Menü)
    def on_resume_button_click(self, on_click):
        return Button(
            scale=(.22, .09),
            y=.12,
            color=color.lime,
            highlight_color=color.hex('#84e35c'),
            pressed_color=color.hex('#5fbf2f'),
            highlight_scale=1.05,
            text='Fortsetzen',
            text_size=1.3,
            text_color=color.white,
            on_click=on_click
        )

    
    # Start Button(Start Menü)
    def on_play_button_click(self, on_click):
        return Button(
            scale=(.22, .09),
            color=color.hex('#16a34a'),
            highlight_color=color.hex('#22c55e'),
            pressed_color=color.hex('#15803d'),
            highlight_scale=1.05,
            text='Spiel starten',
            text_size=1.3,
            text_color=color.white,
            on_click=on_click
        )
    

    # Spielmodi Button(Start Menü)
    def on_gamemode_button_click(self, on_click):
        return Button(
            scale=(.22, .09),
            y=-.12,
            color=color.hex('#4b5563'),
            highlight_color=color.hex('#6b7280'),
            pressed_color=color.hex('#374151'),
            highlight_scale=1.05,
            text='Spielmodi',
            text_size=1.1,
            text_color=color.white,
            on_click=on_click
        )


    # Einstellungen Button(Start Menü und Pause Menü)
    def on_settings_button_click(self, on_click):
        #self.on_play_button_click.disabled = True
        #self.exit_game.disabled = True
        return Button(
            scale=(.16, .06),
            x=.82,
            y=.45,
            color=color.hex('#374151'),
            highlight_color=color.hex('#6b7280'),
            pressed_color=color.hex('#1f2937'),
            highlight_scale=1.05,
            text='⚙️',
            text_size=1,
            text_color=color.white,
            on_click=on_click
        )