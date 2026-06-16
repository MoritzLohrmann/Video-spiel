from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from controls import PlayerController
from Funktions import allFunktions


class Menu(Entity):
    def __init__(self):
        super().__init__()
        Cursor()
        Button.default_color = color.red
        self.b = Button(
            model='quad',
            scale=.05,
            x=-.5,
            color=color.lime,
            text='Start game',
            text_size=.5,
            text_color=color.black,
            on_click=self.remove
        )
        self.player = None
        self.controller = PlayerController()
        self.functions = allFunktions()
        self.exit_button = None
        self.camara = camera

        ##editor_camera = EditorCamera(enabled=False, ignore_paused=True)
        

    def show_fps(self):
        fps = int(1 / time.dt)
        print(f"FPS: {fps}")

    def remove(self):
        self.b.disable()

        self.ground = Entity(model='raum01.blend',collider='mesh',position=(0, -1, 0))
        ##self.block = Entity(model='tomogatie v2.obj', texture='test tommogatixccolor.png' , collision = 'box', scale=(1, 2, 1), position=(0, 0, -5), color=color.white)
        #self.player = Entity(model='cube', z=-10, color=color.orange, origin_y=.5, speed=8, collider='box')

        self.player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
        #self.player.collider = BoxCollider(self.player, Vec3(0,1,0), Vec3(1,2,1))
       ## self.player.collider = BoxCollider(self.player, Vec3(0,1,0), Vec3(1,2,1))
        ##self.controller.attach(self.player)
        #mouse.locked = True
    
 
   # def movement(self):
        #speed = 5
        #movement = Vec3(
           # held_keys['d'] - held_keys['a'],
           # 0,
           # held_keys['w'] - held_keys['s']
        #)
        #self.camera.position += (camera.right * movement.x + camera.forward * movement.z) * speed * time.dt
 

    def input(self, key):
        if key == 'escape':
            if self.exit_button is None:
                self.exit_button = self.functions.on_button_click(key)
                mouse.locked = False
            else:
                self.exit_button.disable()
                self.exit_button = None
                mouse.locked = True
        if key == 'u':
            self.shoot()

    def update(self):
        if self.player:
            self.controller.update()
            camera.rotation_y += mouse.velocity[0] * 1000 * time.dt
            camera.rotation_x -= mouse.velocity[1] * 1000 * time.dt
            camera.rotation_x = clamp(camera.rotation_x, -90, 90)

    def shoot(self):
        origin=self.player.world_position + Vec3(0,0,10)
        flugbahn=raycast(origin,camera.forward,debug=True)
        


def start():
    app = Ursina(title="3d", borderless=False)
    menu = Menu()
    app.run()
