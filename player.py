import ThreeD
from ThreeD import *


class Player:
    def __init__(self):
        self.list_place = ThreeD.cube_place[random.randint(0, len(ThreeD.cube_place))]
        self.side_vel = 0
        self.forward_vel = 0
        self.up_vel = 0
        self.x = self.list_place[0]
        self.y = self.list_place[1] - 10
        self.z = self.list_place[2]

    def respawn(self):
        self.side_vel = 0
        self.forward_vel = 0
        self.up_vel = 0
        self.x = self.list_place[0]
        self.y = self.list_place[1] - 20
        self.z = self.list_place[2]

    def collide(self, lst, y_diff=0):
        lst = close(lst, (self.x, self.y, self.z))
        return ThreeD.collision(lst, (self.x, self.y+y_diff, self.z), 3, 1)

    def collide_side(self, angle_y):
        self.side_vel *= -1
        self.z += math.sin(angle_y) * self.side_vel
        self.x -= math.cos(angle_y) * self.side_vel
        self.side_vel = 0

    def collide_forward(self, angle_y):
        self.forward_vel *= -1
        self.z -= math.cos(angle_y) * self.forward_vel
        self.x -= math.sin(angle_y) * self.forward_vel
        self.forward_vel = 0

    def collide_y(self):
        self.up_vel *= -1
        self.y += self.up_vel
        self.up_vel = 0

    def set_side_vel(self, amount):
        self.side_vel = amount

    def set_forward_vel(self, amount):
        self.forward_vel = amount

    def change_forward_vel(self, amount):
        self.forward_vel += amount

    def change_side_vel(self, amount):
        self.side_vel += amount

    def set_up_vel(self, amount):
        self.up_vel = amount

    def move_forward(self, amount, angle_y):
        self.forward_vel += amount
        self.z -= math.cos(angle_y) * self.forward_vel
        self.x -= math.sin(angle_y) * self.forward_vel

    def move_side(self, amount, angle_y):
        self.side_vel += amount
        self.z += math.sin(angle_y) * self.side_vel
        self.x -= math.cos(angle_y) * self.side_vel

    def move_up(self, amount):
        self.up_vel += amount
        if self.up_vel > 2:
            self.up_vel = 2
        self.y += self.up_vel

    def slow_side(self, angle_y):
        self.side_vel *= .8
        self.z += math.sin(angle_y) * self.side_vel
        self.x -= math.cos(angle_y) * self.side_vel

    def slow_forward(self, angle_y):
        self.forward_vel *= .8
        self.z -= math.cos(angle_y) * self.forward_vel
        self.x -= math.sin(angle_y) * self.forward_vel

    def gravity(self):
        self.up_vel += .1
        if self.up_vel > 2:
            self.up_vel = 2

    def get_origin(self):
        return self.x, self.y, self.z
