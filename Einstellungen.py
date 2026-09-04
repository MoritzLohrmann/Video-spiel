from ursina import *


class Einstellungen(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused=True, **kwargs)

        Text(
            parent=self,
            text='Einstellungen',
            y=.11,
            origin=(0, 0),
            scale=1.5,
        )

        volume_slider = Slider(
            0, 1,
            default=Audio.volume_multiplier,
            step=.05,
            dynamic=True,
            text='Lautstärke',
            parent=self,
            x=-.22,
            y=-.02,
            ignore_paused=True,
        )

        def set_volume(slider=volume_slider):
            Audio.volume_multiplier = slider.value
        volume_slider.on_value_changed = set_volume
