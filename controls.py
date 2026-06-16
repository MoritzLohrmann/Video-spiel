from ursina import Vec3, camera, held_keys, mouse, time, clamp


class PlayerController:
    def __init__(self, speed=5):
        self.player = None
        self.speed = speed

    def attach(self, player):
        self.player = player

    def update(self):
        if self.player is None:
            return

        movement = Vec3(
            held_keys['d'] - held_keys['a'],
            0,
            held_keys['w'] - held_keys['s']
        )
        origin = self.world_position + (self.up*.5) 
        hit_info = raycast(origin , self.direction, ignore=(self,), distance=.5, debug=False)
        if not hit_info.hit:
            
            camera.position += (camera.right * movement.x + camera.forward * movement.z) * self.speed * time.dt

            camera.rotation_y += mouse.velocity[0] * 1000 * time.dt
            camera.rotation_x -= mouse.velocity[1] * 1000 * time.dt
            camera.rotation_x = clamp(camera.rotation_x, -90, 90)
