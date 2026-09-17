from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from Funktions import allFunktions

class Player(FirstPersonController):
    def __init__(self, max_health=100, death_y=-10, **kwargs):
        super().__init__(**kwargs)
        self.functions = allFunktions()
        self.gun = None
         # UI-Anzeige für Munition/Reload
        self.ammo_text = Text(parent=camera.ui,text="0 / 0", position=window.bottom_right + Vec2(-0.3, 0.1),origin=(0, 0),scale=2,color=color.orange)

        self.is_dead = False
        self.max_health = max_health
        self.health = max_health
        self.health_text = Text(parent=camera.ui, text=self.get_health_string(),
                                 position=window.bottom_left + Vec2(0.1, 0.1),
                                 origin=(0, 0), scale=2, color=color.red)

        self.spawn_position = self.position
        self.death_y = death_y

# Respawn Point -> für später hier Ändern.        
        self.respawn_position = Vec3(0, 0, 0)

    def input(self, key):
        if self.is_dead:
            return

        super().input(key)

        # Schießen läuft über Gun.update() (Dauerfeuer), nicht über input()

        if key == 'r' and self.gun:
            self.gun.reload()

    def pickupGun(self, gun):
        gun.parent = camera
        gun.position = Vec3(0.4, -0.5, 1)
        self.gun = gun
        self.setAmmoText(gun.get_ammo_string())
        gun.collider = None

    def setAmmoText(self, text):
        self.ammo_text.text = text

    def get_health_string(self):
        return f'{self.health}/{self.max_health}'

    def take_damage(self, amount):
        if self.is_dead:
            return
        self.health = max(0, self.health - amount)
        self.health_text.text = self.get_health_string()
        if self.health <= 0:
            self.die()

    def die(self):
        if self.is_dead:
            return
        self.is_dead = True
        self.health = 0
        self.health_text.text = self.get_health_string()
        mouse.locked = False

        self.death_overlay = Entity(parent=camera.ui, model='quad', scale=2, color=color.black66, z=1)
        self.death_text = Text(parent=camera.ui, text='Da bist du gestorben :^)', origin=(0, 0),
                                scale=3, color=color.red, y=.1, z=-1)
        self.respawn_button = self.functions.on_respawn_button_click(self.respawn)

    def respawn(self):
        if not self.is_dead:
            return

        death_position = self.position

        self.is_dead = False
        self.health = self.max_health
        self.health_text.text = self.get_health_string()

        self.position = self.respawn_position
        self.rotation_y = 0
        self.camera_pivot.rotation_x = 0

        if self.gun:
            gun = self.gun
            gun.parent = scene
            gun.position = death_position
            gun.collider = 'box'
            self.gun = None
        self.setAmmoText('0 / 0')

        destroy(self.death_overlay)
        self.death_overlay = None
        destroy(self.death_text)
        self.death_text = None
        destroy(self.respawn_button)
        self.respawn_button = None

        mouse.locked = True

    def update(self):
        if self.is_dead:
            return

        super().update()

        if self.position.y < self.death_y:
            self.die()