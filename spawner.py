from ursina import *
import random

from enemy import Enemy
from enemy_types import ENEMY_TYPES
from waves import get_wave


class EnemySpawner(Entity):
    BREAK_DURATION = 5
    MIN_SPAWN_DISTANCE = 10
    MAX_SPAWN_DISTANCE = 40
    VIEW_DOT_THRESHOLD = .5  # entspricht ca. 60° um die Blickrichtung
    STRAGGLER_TIME = 20  # Sekunden ohne Sichtkontakt, bis ein Gegner näher versetzt wird

    def __init__(self, player, spawn_points):
        super().__init__()
        self.player = player
        self.spawn_points = []
        self.markers = []
        self.markers_visible = False

        # Die Gegner behalten eine Referenz auf diese Liste, sie darf also nie neu zugewiesen werden
        self.alive = []
        self.spawn_queue = []

        self.wave_number = 1
        self.wave = None
        self.wave_state = 'break'
        self.break_timer = self.BREAK_DURATION
        self.spawn_timer = 0

        self.wave_text = Text(parent=camera.ui, origin=(-.5, .5), scale=1.5, color=color.white)
        self.last_aspect_ratio = None
        self.update_wave_text()

        self.add_spawn_points(spawn_points)

    # Schnittstelle für den Map-Generator: Spawnpunkte kommen immer von außen
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

        # Die Timer laufen hier statt über invoke, weil update() bei application.paused automatisch stoppt
        if self.player.is_dead:
            return

        if self.wave_state == 'break':
            self.update_break()
        elif self.wave_state == 'spawning':
            self.update_spawning()
        elif self.wave_state == 'fighting':
            self.update_fighting()

        self.relocate_stragglers()

    def update_break(self):
        self.break_timer -= time.dt
        if self.break_timer <= 0:
            self.start_wave()

    def update_spawning(self):
        self.spawn_timer -= time.dt
        if self.spawn_timer > 0:
            return

        # Ohne Spawnpunkte wird gewartet, bis der Map-Generator welche liefert
        if len(self.alive) >= self.wave.max_alive or not self.spawn_points:
            return

        self.spawn_enemy(self.spawn_queue.pop(), self.pick_spawn_point())
        self.spawn_timer = self.wave.spawn_interval

        if not self.spawn_queue:
            self.wave_state = 'fighting'

    def update_fighting(self):
        if not self.alive:
            self.wave_number += 1
            self.start_break()

    def start_break(self):
        self.wave_state = 'break'
        self.break_timer = self.BREAK_DURATION
        self.update_wave_text()

    def start_wave(self):
        self.wave = get_wave(self.wave_number)

        self.spawn_queue = []
        for type_name, count in self.wave.enemies.items():
            for _ in range(count):
                self.spawn_queue.append(type_name)
        random.shuffle(self.spawn_queue)

        self.spawn_timer = 0
        self.wave_state = 'spawning'
        self.update_wave_text()

    def restart_wave(self):
        for enemy in self.alive:
            enemy.despawn()
        self.alive.clear()
        self.spawn_queue = []
        self.start_break()

    # Einzelner Spawn ohne Wellenlogik, darauf kann später ein raumbasierter Modus aufbauen
    def spawn_enemy(self, type_name, position):
        enemy = Enemy(player=self.player, enemy_type=ENEMY_TYPES[type_name], hp_multiplier=self.wave.hp_multiplier,
                      on_death=self.on_enemy_death, position=position)
        enemy.neighbors = self.alive
        self.alive.append(enemy)
        self.update_wave_text()

    def on_enemy_death(self, enemy):
        self.alive.remove(enemy)
        self.update_wave_text()

    def is_seen_by_player(self, point):
        target = point + Vec3(0, 1, 0)
        to_target = target - camera.world_position
        direction = to_target.normalized()

        if direction.dot(camera.forward) < self.VIEW_DOT_THRESHOLD:
            return False

        # Im Sichtfeld, aber eine Wand dazwischen zählt ebenfalls als nicht sichtbar
        hit_info = raycast(camera.world_position, direction, distance=to_target.length(),
                           ignore=(self.player, *self.alive))
        return not hit_info.hit

    def is_valid_spawn_point(self, point):
        dist = distance_xz(self.player.position, point)
        if dist < self.MIN_SPAWN_DISTANCE or dist > self.MAX_SPAWN_DISTANCE:
            return False
        return not self.is_seen_by_player(point)

    def get_valid_spawn_points(self):
        valid_points = []
        for point in self.spawn_points:
            if self.is_valid_spawn_point(point):
                valid_points.append(point)
        return valid_points

    def pick_spawn_point(self):
        valid_points = self.get_valid_spawn_points()
        if valid_points:
            return random.choice(valid_points)

        # Es darf nie keinen Spawn geben, deshalb bleibt als Notlösung der entfernteste Punkt
        return max(self.spawn_points, key=lambda point: distance_xz(self.player.position, point))

    def relocate_stragglers(self):
        # Gegner laufen nur bei Sichtkontakt los. Ohne das könnte eine Welle ewig offen bleiben,
        # weil irgendwo noch ein Gegner hinter einer Wand steht.
        for enemy in self.alive:
            if enemy.time_without_sight < self.STRAGGLER_TIME:
                continue
            enemy.time_without_sight = 0

            valid_points = self.get_valid_spawn_points()
            if not valid_points:
                continue

            nearest = min(valid_points, key=lambda point: distance_xz(self.player.position, point))
            # Nur versetzen, wenn der Gegner dadurch wirklich näher kommt
            if distance_xz(self.player.position, nearest) < distance_xz(self.player.position, enemy.position):
                enemy.position = nearest

    def update_wave_text(self):
        remaining = len(self.alive) + len(self.spawn_queue)
        self.wave_text.text = f'Welle {self.wave_number} – Gegner: {remaining}'

    def layout_ui(self):
        # Wie im Player: Die Fensterränder ändern sich mit dem Seitenverhältnis
        self.wave_text.position = window.top_left + Vec2(.03, -.03)

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
