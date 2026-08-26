from ursina import *
from ursina.prefabs.health_bar import HealthBar
from direct.actor.Actor import Actor


class Enemy(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(model='cube', scale_y=1, origin_y=-.5, color=color.light_gray, collider='box', **kwargs)

        self.player = player  # Referenz auf den Spieler, statt globaler Variable

        # Fehlte komplett: Actor tatsächlich laden
       # self.actor = Actor(
       #     'Enemys/sk_spider.fbx',
        #    {'walk': 'Enemys/sk_spider_move.fbx'}
       # )
       # self.actor.reparentTo(self)
       # self.actor.setScale(1)
        # self.actor.loop('idle')  # Startzustand: Leerlaufanimation in Schleife

        self.origin_y = -.5
        self.scale_y = 2
        self.color = color.light_gray

        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5, .1, .1))
        self.max_hp = 100
        self.hp = self.max_hp

        self.is_walking = False


        self.attack_damage = 10
        self.attack_rate = 1.0  
        self.can_attack = True  



    def update(self):
        dist = distance_xz(self.player.position, self.position)
        if dist > 40:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        self.look_at_2d(self.player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0, 1, 0), self.forward, 30, ignore=(self,))

        if hit_info.entity == self.player:
            if dist > 2:
                self.position += self.forward * time.dt * 5
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

    def reset_can_attack(self):
        self.can_attack = True  

    

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            destroy(self)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1