from ursina import *
from ursina.prefabs.ursfx import ursfx
import random


class Gun(Button):
    def __init__(self, player, damage=10, fire_rate=0.3, magazine_size=12, reload_time=1, max_range=100,
                 muzzle_offset=Vec3(0, 0, 1), recoil=1.5, model='cube', gun_color=color.blue, collider='box',
                 origin_y=-.5, scale=(.2, .2, 1), **kwargs):
        super().__init__(model=model, color=gun_color, origin_y=origin_y, collider=collider, scale=scale, **kwargs)
        self.player = player
        self.damage = damage
        self.fire_rate = fire_rate
        self.magazine_size = magazine_size
        self.ammo = magazine_size
        self.reload_time = reload_time
        self.max_range = max_range
        self.recoil = recoil
        self.is_reloading = False
        self.can_shoot = True
        self.wait_for_release = False
        self.muzzle = Entity(parent=self, position=muzzle_offset)

        # treffer erkannt
        self.hitmarker = Entity(parent=camera.ui, enabled=False)
        for rotation_z in (45, -45):
            Entity(parent=self.hitmarker, model='quad', color=color.white,
                   scale=(.03, .004), rotation_z=rotation_z)

    def update(self):
        if self.player.gun is not self or self.player.is_dead:
            return

        if self.wait_for_release:
            if not held_keys['left mouse']:
                self.wait_for_release = False
            return

        if held_keys['left mouse']:
            self.shoot()

    def shoot(self):
        if self.is_reloading or not self.can_shoot:
            return

        if self.ammo == 0:
            self.reload()
            return

        self.ammo -= 1
        self.update_ui()

#lösung für den rückstoß -> zeitpunkt des schusses merken + waffe nach oben und dann wieder runter. (bekomme die Animation von Blender nicht hin, daher so)
        hit_info = raycast(camera.world_position, camera.forward, distance=self.max_range, ignore=(self.player, self))
        if hit_info.hit:
            target_point = hit_info.world_point
            self.spawn_impact(hit_info)
            if hasattr(hit_info.entity, 'hp'):
                hit_info.entity.blink(color.red)
                hit_info.entity.hp -= self.damage
                self.show_hitmarker()
        else:
            target_point = camera.world_position + camera.forward * self.max_range

        self.spawn_tracer(target_point)
        self.play_shot_sound()
        self.apply_recoil()

#schuss verzögern
        self.can_shoot = False
        invoke(self.reset_can_shoot, delay=self.fire_rate)

        if self.ammo == 0:
            self.reload()

    def spawn_tracer(self, target_point):
        bullet = Entity(model='cube', scale=(.04, .04, .6), color=color.black, position=self.muzzle.world_position)
        bullet.look_at(target_point)
        travel_time = max(.05, distance(bullet.position, target_point) / 300)
        bullet.animate_position(target_point, curve=curve.linear, duration=travel_time)
        destroy(bullet, delay=travel_time)

    def spawn_impact(self, hit_info):
        if hit_info.world_normal is None:
            return

        impact = Entity(model='quad', scale=.1, color=color.dark_gray, double_sided=True,
                        position=hit_info.world_point + hit_info.world_normal * .01)
        impact.look_at(impact.position + hit_info.world_normal)
        impact.fade_out(duration=.4, delay=.6)
        destroy(impact, delay=1)

    def show_hitmarker(self):
        self.hitmarker.enabled = True
        invoke(self.hide_hitmarker, delay=.1)

    def hide_hitmarker(self):
        self.hitmarker.enabled = False



    def apply_recoil(self):
        # Kurzer Kick nach oben
        pivot = self.player.camera_pivot
        start_rotation = pivot.rotation_x
        pivot.rotation_x = clamp(start_rotation - self.recoil, -90, 90)
        pivot.animate_rotation_x(start_rotation, duration=.12, curve=curve.out_quad)

    def play_shot_sound(self):
        ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)],
              volume=.5, wave='noise', pitch=random.uniform(-13, -12), pitch_change=-12, speed=3.0)

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
