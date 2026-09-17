from ursina import *
from ursina.prefabs.ursfx import ursfx


class Einstellungen(Entity):
    # Master-Lautstärke in Prozent (0-100). Klassenattribut, damit der Wert erhalten
    # bleibt, wenn das Panel geschlossen wird, und in Startmenü wie Pausemenü gilt.
    volume_percent = int(Audio.volume_multiplier * 100)

    @classmethod
    def apply_volume(cls, percent):
        cls.volume_percent = int(clamp(round(percent), 0, 100))
        volume = cls.volume_percent / 100

        # Gilt für alle künftig erzeugten Sounds
        Audio.volume_multiplier = volume

        # Bereits laufende Sounds rechnen den Multiplikator nur beim Setzen ihrer
        # Lautstärke ein, deshalb hier einmal neu durchreichen -> wirkt sofort.
        for entity in scene.entities:
            if isinstance(entity, Audio):
                entity.volume = entity.volume

    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused=True, **kwargs)

        Text(
            parent=self,
            text='Einstellungen',
            y=.11,
            origin=(0, 0),
            scale=1.5,
        )

        self.volume_slider = Slider(
            0, 100,
            default=Einstellungen.volume_percent,
            step=1,
            dynamic=True,
            text='Lautstärke',
            parent=self,
            x=-.22,
            y=-.02,
            ignore_paused=True,
        )
        
        self.volume_slider.knob.ignore_paused = True
        self.volume_slider.bg.ignore_paused = True
        self.volume_slider.on_value_changed = self.on_volume_changed

       #Test ton
        #self.test_button = Button(
        #    parent=self,
        #    text='Test',
        #    scale=(.1, .05),
        #    x=0,
        #    y=-.12,
        #    color=color.hex('#374151'),
        #    highlight_color=color.hex('#6b7280'),
        #    pressed_color=color.hex('#1f2937'),
        #    ignore_paused=True,
        #    on_click=self.play_test_sound,
        #)

    def on_volume_changed(self):
        Einstellungen.apply_volume(self.volume_slider.value)

    def play_test_sound(self):
        # ignore_paused, sonst bleibt der Testton im Pausemenü stumm
        ursfx(
            [(0.0, 0.0), (0.05, 1.0), (0.2, 0.6), (0.4, 0.3), (0.6, 0.0)],
            wave='sine',
            pitch=6,
            speed=2.0,
            ignore_paused=True,
        )
