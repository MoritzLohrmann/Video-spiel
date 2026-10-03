from ursina import *
from ursina.prefabs.ursfx import ursfx
from ursina.prefabs.first_person_controller import FirstPersonController


class Einstellungen(Entity):
    MOUSE_SENSITIVITY_MIN = 10
    MOUSE_SENSITIVITY_MAX = 200

    volume_percent = int(Audio.volume_multiplier * 100)     # Lautstärke in %
    mouse_sensitivity = 40      # Standardwert von FirstPersonController
    fullscreen = False

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

    @classmethod
    def apply_mouse_sensitivity(cls, value):
        cls.mouse_sensitivity = int(clamp(round(value), cls.MOUSE_SENSITIVITY_MIN, cls.MOUSE_SENSITIVITY_MAX))

        # Laufenden Player sofort anpassen (neue Player übernehmen den Wert im __init__)
        for entity in scene.entities:
            if isinstance(entity, FirstPersonController):
                entity.mouse_sensitivity = Vec2(cls.mouse_sensitivity, cls.mouse_sensitivity)

    @classmethod
    def apply_fullscreen(cls, value):
        cls.fullscreen = bool(value)
        window.fullscreen = cls.fullscreen

    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused=True, **kwargs)

        Text(
            parent=self,
            text='Einstellungen',
            y=.2,
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
            y=.08,
            ignore_paused=True,
        )
        self.volume_slider.knob.ignore_paused = True
        self.volume_slider.bg.ignore_paused = True
        self.volume_slider.on_value_changed = self.on_volume_changed

        self.sensitivity_slider = Slider(
            Einstellungen.MOUSE_SENSITIVITY_MIN, Einstellungen.MOUSE_SENSITIVITY_MAX,
            default=Einstellungen.mouse_sensitivity,
            step=1,
            dynamic=True,
            text='Maus',
            parent=self,
            x=-.22,
            y=-.01,
            ignore_paused=True,
        )
        self.sensitivity_slider.knob.ignore_paused = True
        self.sensitivity_slider.bg.ignore_paused = True
        self.sensitivity_slider.on_value_changed = self.on_sensitivity_changed

        self.fullscreen_button = Button(
            parent=self,
            text=self.get_fullscreen_text(),
            scale=(.22, .06),
            y=-.12,
            color=color.hex('#374151'),
            highlight_color=color.hex('#6b7280'),
            pressed_color=color.hex('#1f2937'),
            ignore_paused=True,
            on_click=self.toggle_fullscreen,
        )

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

    def on_sensitivity_changed(self):
        Einstellungen.apply_mouse_sensitivity(self.sensitivity_slider.value)

    def get_fullscreen_text(self):
        return 'Vollbild: An' if Einstellungen.fullscreen else 'Vollbild: Aus'

    def toggle_fullscreen(self):
        Einstellungen.apply_fullscreen(not Einstellungen.fullscreen)
        self.fullscreen_button.text = self.get_fullscreen_text()

    def play_test_sound(self):
        # ignore_paused, sonst bleibt der Testton im Pausemenü stumm
        ursfx(
            [(0.0, 0.0), (0.05, 1.0), (0.2, 0.6), (0.4, 0.3), (0.6, 0.0)],
            wave='sine',
            pitch=6,
            speed=2.0,
            ignore_paused=True,
        )
