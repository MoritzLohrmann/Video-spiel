from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gun = None
         # UI-Anzeige für Munition/Reload
        self.ammo_text = Text(parent=camera.ui,text="0 / 0", position=window.bottom_right + Vec2(-0.3, 0.1),origin=(0, 0),scale=2,color=color.orange)


    def input(self, key):
        super().input(key)  

        if key == 'left mouse down' and self.gun:
            self.gun.shoot()
            if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
                mouse.hovered_entity.hp -= 10
                mouse.hovered_entity.blink(color.red)

        if key == 'r' and self.gun:
            self.gun.reload()

    def pickupGun(self, gun):
        gun.parent = camera
        gun.position = Vec3(.5, -0.2, .5)
        self.gun = gun
        self.setAmmoText(gun.get_ammo_string())

    def setAmmoText(self, text):
        self.ammo_text.text = text