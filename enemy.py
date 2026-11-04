from ursina import *
from ursina.prefabs.health_bar import HealthBar
from direct.actor.Actor import Actor
import random


class Enemy(Entity):
    SEPARATION_DISTANCE = 1.2
    SEPARATION_SPEED = 3

    def __init__(self, player, enemy_type, hp_multiplier=1.0, on_death=None, **kwargs):
        super().__init__(model=enemy_type.model, scale=enemy_type.scale, origin_y=-.5, color=enemy_type.color,
                         collider='box', **kwargs)

        self.player = player
        self.enemy_type = enemy_type
        self.on_death = on_death
        self.is_dead = False
        self.nachbarn = []

        # Fehlte komplett: Actor tatsächlich laden
       # self.actor = Actor(
       #     'Enemys/sk_spider.fbx',
        #    {'walk': 'Enemys/sk_spider_move.fbx'}
       # )
       # self.actor.reparentTo(self)
       # self.actor.setScale(1)
        # self.actor.loop('idle')  # Startzustand: Leerlaufanimation in Schleife

        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5, .2, .1))
        self.max_hp = enemy_type.max_hp * hp_multiplier
        self.hp = self.max_hp

        self.is_walking = False

        self.ohne_sicht = 0

        self.attack_damage = enemy_type.attack_damage
        self.attack_rate = enemy_type.attack_rate
        self.can_attack = True



    def update(self):
        self.keep_distance_to_neighbors()
        self.ohne_sicht += time.dt

        dist = distance_xz(self.player.position, self.position)
        if dist > self.enemy_type.sight_range:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        self.look_at_2d(self.player.position, 'y')
        # Andere Gegner ignorieren, sonst bleibt jeder stehen, der hinter einem anderen läuft
        hit_info = raycast(self.world_position + Vec3(0, 1, 0), self.forward, self.enemy_type.sight_range,
                           ignore=(self, *self.nachbarn))

        if hit_info.entity == self.player:
            self.ohne_sicht = 0
            if dist > self.enemy_type.attack_range:
                self.position += self.forward * time.dt * self.enemy_type.speed
                if not self.is_walking:
                    #self.actor.loop('walk')
                    self.is_walking = True
            else:
                if self.is_walking:
                    #self.actor.loop('idle')
                    self.is_walking = False
                if self.can_attack:
                    self.player.take_damage(self.attack_damage)
                    self.can_attack = False
                    invoke(self.reset_can_attack, delay=self.attack_rate)
        else:
            if self.is_walking:
                #self.actor.loop('idle')
                self.is_walking = False

#versucht!! das die gegner nicht ineinander hängen

    def keep_distance_to_neighbors(self):
        for anderer in self.nachbarn:
            if anderer is self:
                continue

            abstand = Vec3(self.x - anderer.x, 0, self.z - anderer.z)
            if abstand.length() >= self.SEPARATION_DISTANCE:
                continue

            if abstand.length() == 0:
                abstand = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1))

            self.position += abstand.normalized() * self.SEPARATION_SPEED * time.dt

    def reset_can_attack(self):
        if self.is_dead:
            return
        self.can_attack = True

    def die(self):
        if self.is_dead:
            return
        self.is_dead = True
        if self.on_death:
            self.on_death(self)
        destroy(self)

    def despawn(self):
        self.is_dead = True
        destroy(self)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            self.die()
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1
