from ursina import *
import random

from enemy import Enemy
from enemy_types import ENEMY_TYPES
from waves import get_wave


class EnemySpawner(Entity):
    BREAK_DURATION = 5
    MIN_SPAWN_DISTANCE = 10
    MAX_SPAWN_DISTANCE = 40
    VIEW_DOT_THRESHOLD = .5 
    STRAGGLER_TIME = 20  

    def __init__(self, player, spawn_points):
        super().__init__()
        self.player = player
        self.spawn_points = []
        self.markers = []
        self.markers_visible = False


        self.lebende = []
        self.warteschlange = []

        self.wellen_nr = 1
        self.welle = None
        self.status = 'break'
        self.pausen_timer = self.BREAK_DURATION
        self.spawn_timer = 0

        self.wellen_text = Text(parent=camera.ui, origin=(-.5, .5), scale=1.5, color=color.white)
        self.last_aspect_ratio = None
        self.update_wave_text()

        self.add_spawn_points(spawn_points)

   
    def add_spawn_points(self, points):
        for point in points:
            self.spawn_points.append(Vec3(*point))
        self.rebuild_markers()

    def clear_spawn_points(self):
        self.spawn_points.clear()
        self.rebuild_markers()

    def update(self):
        if camera.aspect_ratio != self.last_aspect_ratio:
            self.last_aspect_ratio = camera.aspect_ratio
            self.layout_ui()

        
        if self.player.is_dead:
            return

        if self.status == 'break':
            self.update_break()
        elif self.status == 'spawning':
            self.update_spawning()
        elif self.status == 'fighting':
            self.update_fighting()

        self.relocate_stragglers()

    def update_break(self):
        self.pausen_timer -= time.dt
        if self.pausen_timer <= 0:
            self.start_wave()

    def update_spawning(self):
        self.spawn_timer -= time.dt
        if self.spawn_timer > 0:
            return

        
        if len(self.lebende) >= self.welle.max_alive or not self.spawn_points:
            return

        self.spawn_enemy(self.warteschlange.pop(), self.pick_spawn_point())
        self.spawn_timer = self.welle.spawn_interval

        if not self.warteschlange:
            self.status = 'fighting'

    def update_fighting(self):
        if not self.lebende:
            self.wellen_nr += 1
            self.start_break()

    def start_break(self):
        self.status = 'break'
        self.pausen_timer = self.BREAK_DURATION
        self.update_wave_text()

    def start_wave(self):
        self.welle = get_wave(self.wellen_nr)

        self.warteschlange = []
        for type_name, count in self.welle.enemies.items():
            for _ in range(count):
                self.warteschlange.append(type_name)
        random.shuffle(self.warteschlange)

        self.spawn_timer = 0
        self.status = 'spawning'
        self.update_wave_text()

    def restart_wave(self):
        for enemy in self.lebende:
            enemy.despawn()
        self.lebende.clear()
        self.warteschlange = []
        self.start_break()

    def spawn_enemy(self, type_name, position):
        enemy = Enemy(player=self.player, enemy_type=ENEMY_TYPES[type_name], hp_multiplier=self.welle.hp_multiplier,
                      on_death=self.on_enemy_death, position=position)
        enemy.nachbarn = self.lebende
        self.lebende.append(enemy)
        self.update_wave_text()

    def on_enemy_death(self, enemy):
        self.lebende.remove(enemy)
        self.update_wave_text()

    def is_seen_by_player(self, point):
        ziel = point + Vec3(0, 1, 0)
        zum_ziel = ziel - camera.world_position
        richtung = zum_ziel.normalized()

        if richtung.dot(camera.forward) < self.VIEW_DOT_THRESHOLD:
            return False

        # Im Sichtfeld, aber eine Wand dazwischen zählt ebenfalls als nicht sichtbar
        hit_info = raycast(camera.world_position, richtung, distance=zum_ziel.length(),
                           ignore=(self.player, *self.lebende))
        return not hit_info.hit

    def is_valid_spawn_point(self, point):
        dist = distance_xz(self.player.position, point)
        if dist < self.MIN_SPAWN_DISTANCE or dist > self.MAX_SPAWN_DISTANCE:
            return False
        return not self.is_seen_by_player(point)

    def get_valid_spawn_points(self):
        gueltige = []
        for point in self.spawn_points:
            if self.is_valid_spawn_point(point):
                gueltige.append(point)
        return gueltige

    def pick_spawn_point(self):
        gueltige = self.get_valid_spawn_points()
        if gueltige:
            return random.choice(gueltige)

        # Es darf nie keinen Spawn geben, deshalb bleibt als Notlösung der entfernteste Punkt
        return max(self.spawn_points, key=lambda point: distance_xz(self.player.position, point))

    def relocate_stragglers(self):
        # Gegner laufen nur bei Sichtkontakt los. Ohne das könnte eine Welle ewig offen bleiben,
        # weil irgendwo noch ein Gegner hinter einer Wand steht.
        for enemy in self.lebende:
            if enemy.ohne_sicht < self.STRAGGLER_TIME:
                continue
            enemy.ohne_sicht = 0

            gueltige = self.get_valid_spawn_points()
            if not gueltige:
                continue

            naechster = min(gueltige, key=lambda point: distance_xz(self.player.position, point))
            # Nur versetzen, wenn der Gegner dadurch wirklich näher kommt
            if distance_xz(self.player.position, naechster) < distance_xz(self.player.position, enemy.position):
                enemy.position = naechster

    def update_wave_text(self):
        rest = len(self.lebende) + len(self.warteschlange)
        self.wellen_text.text = f'Welle {self.wellen_nr} – Gegner: {rest}'

    def layout_ui(self):
        # Wie im Player: Die Fensterränder ändern sich mit dem Seitenverhältnis
        self.wellen_text.position = window.top_left + Vec2(.03, -.03)

    def rebuild_markers(self):
        for marker in self.markers:
            destroy(marker)
        self.markers = []

        for point in self.spawn_points:
            marker = Entity(model='sphere', color=color.lime, scale=.5, position=point + Vec3(0, 1, 0),
                            enabled=self.markers_visible)
            self.markers.append(marker)

    def input(self, key):
        # Debug: Spawnpunkte sichtbar machen
        if key == 'f3':
            self.markers_visible = not self.markers_visible
            for marker in self.markers:
                marker.enabled = self.markers_visible
