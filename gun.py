from ursina import *


class Gun(Button):
    def __init__(self,player, damage=10, fire_rate=0.3, magazine_size=12, reload_time=1.5,model='cube',gun_color=color.blue,collider='box', origin_y=-.5,scale=(.2, .2, 1), **kwargs):
        super().__init__(model=model, color=gun_color, origin_y=origin_y, collider=collider, scale=scale, **kwargs)
        self.player = player
        self.damage = damage
        self.fire_rate = fire_rate          
        self.magazine_size = magazine_size
        self.ammo = magazine_size
        self.reload_time = reload_time
        self.is_reloading = False
        self.can_shoot = True

    def shoot(self):
        if self.is_reloading or not self.can_shoot:
            return

        if self.ammo <= 0:
            self.reload()
            return

        self.ammo -= 1
        self.blink(color.orange)
        self.update_ui()

        bullet = Entity(parent=self,model='cube',scale=.1,color=color.black,position=(0,2,1))
        bullet.world_parent = scene
        bullet.animate_position(bullet.position + (bullet.forward * 500),curve=curve.linear,duration=1)
        destroy(bullet, delay=1)

        # Feuerrate: kurze Sperre nach jedem Schuss, also höhere feuerrate -> weniger kugeln pro sekunde, bisschen verwirrend sorry
        self.can_shoot = False
        invoke(self.reset_can_shoot, delay=self.fire_rate)
    
    def get_ammo_string(self):
        if self.is_reloading:
            return 'Reloading...'
        return f'{self.ammo} / {self.magazine_size}'
    
    def update_ui(self):
        self.player.setAmmoText(self.get_ammo_string())

    def reset_can_shoot(self):
        self.can_shoot = True

    def reload(self):
        if self.is_reloading:
            return
        self.is_reloading = True
        self.update_ui()
        invoke(self.finish_reload, delay=self.reload_time)

    def finish_reload(self):
        self.ammo = self.magazine_size
        self.is_reloading = False
        self.update_ui()