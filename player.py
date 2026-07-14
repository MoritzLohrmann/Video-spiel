from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gun = None

    def input(self, key):
        super().input(key)  

        if key == 'left mouse down' and self.gun:
            self.gun.shoot()

        if key == 'r' and self.gun:
            self.gun.reload()

    def pickupGun(self, gun):
        gun.parent = camera
        gun.position = Vec3(.5, -0.2, .5)
        self.gun = gun