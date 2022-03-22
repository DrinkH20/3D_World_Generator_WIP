import random

import pygame
import math
import perlin_noise
from sorting import quicksort
from minimap import draw_map
from main import fill, close
# from player import Player
from main import screen_h, screen_w
import time

plot_cube_place = []
plot_points = []
block_type = []
lines = []

noise = perlin_noise.PerlinNoise()

run = True
angleX = 3.14
angleY = 0
angleZ = 0
rotated = []
rotated_points = []
Y = 0
level_w = 10
level_h = 1
level_d = 20

forward_v = 0
side_v = 0
down_v = 0
first = 0
first_dif_zoom = 350

X = 0
Z = 0

grass = (100, 165, 100)
rock = (100, 100, 100)
wood = (165, 165, 100)
player = (140, 140, 140)
animal = (200, 140, 140)

origin = (10, -20, 10)
past_origin = (origin[0], origin[1], origin[2], player)

distance = 1
cam_x = 250
cam_y = 300

square = 1

repeat = 0

zoom = 350

scrn_w = 500
scrn_h = 500

living_side_vels = []
living_side_time = []
living_forward_vels = []
living_forward_time = []

povX = 0
povY = .1
povZ = 0
povX_dif = 0
povY_dif = .1
povZ_dif = 0

FPS = 0
fps_start = time.time()

window = pygame.display.set_mode((scrn_w, scrn_h))

plot_cube_place.append((origin[0], origin[1], origin[2], player))


# I put this class here because it stopped working in the other file because of a circular import loop
class Player:
    def __init__(self):
        self.list_place = cube_place[random.randint(0, len(cube_place))]
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
        # print(collision(lst, (self.x, self.y+y_diff, self.z), 3, 1))
        return collision(lst, (self.x, self.y+y_diff, self.z), 3, 1)

    def collide_side(self, angle_y):
        self.z -= math.sin(angle_y) * self.side_vel
        self.x += math.cos(angle_y) * self.side_vel
        self.side_vel = 0

    def collide_forward(self, angle_y):
        self.z += math.cos(angle_y) * self.forward_vel
        self.x += math.sin(angle_y) * self.forward_vel
        self.forward_vel = 0

    def collide_y(self):
        self.y += -self.up_vel
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
        self.z += math.sin(-angle_y) * self.side_vel
        self.x -= math.cos(-angle_y) * self.side_vel

    def slow_forward(self, angle_y):
        self.forward_vel *= .8
        self.z -= math.cos(-angle_y) * self.forward_vel
        self.x -= math.sin(-angle_y) * self.forward_vel

    def gravity(self):
        self.up_vel += .1
        if self.up_vel > 2:
            self.up_vel = 2

    def get_origin(self):
        return self.x, self.y, self.z


# This is the code that's supposed to be here
def append(lst, item, m1, m2, m3):
    a = item[0] + m1
    b = item[1] + m2
    c = item[2] + m3
    thing = (a, b, c)
    lst.append(thing)


def draw_poly(p1, p2, p3, p4):
    zm = 0
    if (p1[0] + cam_x < scrn_w + zm) and (p1[0] + cam_x > -zm) \
            and (p1[1] + cam_y < scrn_h + zm) and (p1[1] + cam_y > -zm):
        if (p2[0] + cam_x < scrn_w + zm) and (p2[0] + cam_x > -zm) \
                and (p2[1] + cam_y < scrn_h + zm) and (p2[1] + cam_y > -zm):
            average = (p1[2] + p2[2] + p3[2] + p4[2]) / 4
            if average > (.7 * (zoom / 320)):
                line_size = average / 1
                color_dif = line_size / (zoom / 150)
                if color_dif > 1.1:
                    color_dif = 1.1
                if color == player:
                    if not first:
                        pygame.draw.polygon(window, (color[0] * color_dif, color[1] * color_dif, color[2] * color_dif),
                                            ((p1[0] + cam_x, p1[1] + cam_y),
                                             (p2[0] + cam_x, p2[1] + cam_y),
                                             (p3[0] + cam_x, p3[1] + cam_y),
                                             (p4[0] + cam_x, p4[1] + cam_y)))
                else:
                    pygame.draw.polygon(window, (color[0] * color_dif, color[1] * color_dif, color[2] * color_dif),
                                        ((p1[0] + cam_x, p1[1] + cam_y),
                                         (p2[0] + cam_x, p2[1] + cam_y),
                                         (p3[0] + cam_x, p3[1] + cam_y),
                                         (p4[0] + cam_x, p4[1] + cam_y)))


def draw_line(p1, p2):
    if (p1[0] + cam_x < scrn_w) and (p1[0] + cam_x > 0) and (p1[1] + cam_y < scrn_h) and (p1[1] + cam_y > 0):
        if (p2[0] + cam_x < scrn_w) and (p2[0] + cam_x > 0) and (p2[1] + cam_y < scrn_h) and (p2[1] + cam_y > 0):
            if p1[2] + p2[2] * 3 > 1.5:
                if int(p1[2] + p2[2]) < 30:
                    line_size = p1[2] + p2[2]
                else:
                    line_size = 20
                pygame.draw.line(window, color, (p1[0] + cam_x, p1[1] + cam_y),
                                 (p2[0] + cam_x, p2[1] + cam_y), int(line_size * 3))


def rotate_x(x, y, zx):
    global X
    global Y
    global Z
    X = x
    Y = y * math.cos(angleX) - zx * math.sin(angleX)
    Z = y * math.sin(angleX) + zx * math.cos(angleX)
    return X, Y, Z


def rotate_y(x, y, zy):
    global X
    global Y
    global Z
    X = x * math.cos(angleY) - zy * math.sin(angleY)
    Y = y
    Z = x * math.sin(angleY) + zy * math.cos(angleY)
    return X, Y, Z


def rotate_z(x, y, zz):
    global X
    global Y
    global Z
    X = x * math.cos(angleZ) - y * math.sin(angleZ)
    Y = x * math.sin(angleZ) + y * math.cos(angleZ)
    Z = zz
    return X, Y, Z


def collision(lst, obj, spec=0, dif=0):
    if spec != 0:
        piece = obj[0:spec]
    else:
        piece = obj

    for p in range(len(lst) - dif):
        com = lst[p + dif]
        if p > len(plyr):
            if math.ceil(piece[0] / 2) * 2 == round(com[0]) or math.floor(piece[0] / 2) * 2 == round(com[0]):
                if math.ceil((piece[1]) / 2) * 2 == math.ceil((com[1]) / 2) * 2 or \
                        math.floor((piece[1]) / 2) * 2 == math.floor((com[1]) / 2) * 2:
                    if math.ceil(piece[2] / 2) * 2 == round(com[2]) or math.floor(piece[2] / 2) * 2 == round(com[2]):
                        return 1

    if piece[0] < -1 or piece[0] > screen_w * 2 - 1:
        return 1

    if piece[2] < -1 or piece[2] > screen_h * 2 - 1:
        return 1


cube_place = fill()
plot_cube_place = close(cube_place, origin[0:3])

plyr = [Player()]

while run:
    keys = pygame.key.get_pressed()
    pygame.time.delay(10)
    window.fill((10, 0, 0))

    FPS += 1

    if time.time() - fps_start >= 1:
        fps_start = time.time()
        print("Fps", FPS)
        FPS = 0

    if len(plot_cube_place) < 1:
        plot_cube_place = []
        for itm in range(len(plyr)):
            plot_cube_place.append((plyr[itm].x, plyr[itm].y, plyr[itm].z, animal))
    else:
        if len(plot_cube_place) > len(plyr):
            for itm in range(len(plyr)):
                if itm != 0:
                    plot_cube_place[itm] = (plyr[itm].x, plyr[itm].y, plyr[itm].z, animal)
                else:
                    plot_cube_place[itm] = (plyr[itm].x, plyr[itm].y, plyr[itm].z, player)
        else:
            plot_cube_place[0] = (plyr[0].x, plyr[0].y, plyr[0].z, animal)

    plot_points = []
    for i in plot_cube_place:
        append(plot_points, i, 1, 1, -1)
        append(plot_points, i, -1, 1, -1)
        append(plot_points, i, -1, -1, -1)
        append(plot_points, i, 1, -1, -1)
        append(plot_points, i, 1, 1, 1)
        append(plot_points, i, -1, 1, 1)
        append(plot_points, i, -1, -1, 1)
        append(plot_points, i, 1, -1, 1)

    rotated_points = []
    for i in plot_points:
        rotated = i
        X = 0
        Y = 0
        Z = 0
        origin = plot_cube_place[0]
        if first:
            rotated = rotate_z(rotated[0] - (origin[0] + povX*5),
                               (rotated[1] - (origin[1] + -1.25)),
                               -(rotated[2] - (origin[2] + povZ*5)))
        else:
            rotated = rotate_z(rotated[0] - (origin[0] + (povX * 5) / (abs(povY) * 20)),
                               (rotated[1] - (origin[1] + (povY * 5))),
                               -(rotated[2] - (origin[2] + (povZ * 5) / (abs(povY) * 20))))
        rotated = rotate_x(rotated[0], rotated[1], rotated[2])
        rotated = rotate_y(rotated[0], rotated[1], rotated[2])
        # origin = plot_cube_place[0]
        # rotated = rotated[0] - (origin[0] + povX * 5), \
        #     -rotated[1] - (origin[1] + povY * 5), \
        #     -rotated[2] - (origin[2] + povZ * 5)
        first_dif_zoom = 10
        if first:
            first_dif_zoom = 50
        z = zoom / (350 + rotated[2] * first_dif_zoom)
        rotated_points.append((rotated[0] * 25 * z, rotated[1] * 25 * z, z * 2))

    repeat = 0
    lines = []
    while repeat < len(rotated_points):
        per = plot_cube_place[int(repeat / 8)]
        color = per[3]
        if square:
            lines.append((rotated_points[repeat + 0],
                          rotated_points[repeat + 1],
                          rotated_points[repeat + 2],
                          rotated_points[repeat + 3],
                          color))
            lines.append((rotated_points[repeat + 4],
                          rotated_points[repeat + 5],
                          rotated_points[repeat + 6],
                          rotated_points[repeat + 7],
                          color))
            lines.append((rotated_points[repeat + 2],
                          rotated_points[repeat + 1],
                          rotated_points[repeat + 5],
                          rotated_points[repeat + 6],
                          color))
            lines.append((rotated_points[repeat + 0],
                          rotated_points[repeat + 3],
                          rotated_points[repeat + 7],
                          rotated_points[repeat + 4],
                          color))
            lines.append((rotated_points[repeat + 3],
                          rotated_points[repeat + 2],
                          rotated_points[repeat + 6],
                          rotated_points[repeat + 7],
                          color))
            lines.append((rotated_points[repeat + 1],
                          rotated_points[repeat + 0],
                          rotated_points[repeat + 4],
                          rotated_points[repeat + 5],
                          color))
        else:
            lines.append((rotated_points[repeat + 0], rotated_points[repeat + 1], color))
            lines.append((rotated_points[repeat + 1], rotated_points[repeat + 2], color))
            lines.append((rotated_points[repeat + 2], rotated_points[repeat + 3], color))
            lines.append((rotated_points[repeat + 3], rotated_points[repeat + 0], color))
            lines.append((rotated_points[repeat + 4], rotated_points[repeat + 5], color))
            lines.append((rotated_points[repeat + 5], rotated_points[repeat + 6], color))
            lines.append((rotated_points[repeat + 6], rotated_points[repeat + 7], color))
            lines.append((rotated_points[repeat + 7], rotated_points[repeat + 4], color))
            lines.append((rotated_points[repeat + 4], rotated_points[repeat + 0], color))
            lines.append((rotated_points[repeat + 5], rotated_points[repeat + 1], color))
            lines.append((rotated_points[repeat + 6], rotated_points[repeat + 2], color))
            lines.append((rotated_points[repeat + 7], rotated_points[repeat + 3], color))
        repeat += 8

    s = 0
    e = len(lines) - 1
    lines = quicksort(lines, s, e, 2)

    repeat = 0
    for i in lines:
        if repeat / 12 == round(repeat / 12):
            per = plot_cube_place[int(repeat / 12)]
        if square:
            color = i[4]
            draw_poly(i[0], i[1], i[2], i[3])
        else:
            color = i[2]
            draw_line(i[0], i[1])
        repeat += 1

    origin = list(origin)

    for i in range(len(plyr)):
        if i == 0:
            if keys[pygame.K_d]:
                plyr[i].change_side_vel(-.2)
            if keys[pygame.K_a]:
                plyr[i].change_side_vel(.2)
        else:
            if len(living_side_vels) > i:
                timer = living_side_time[i - 1]
                if timer[1] < time.time() - timer[0]:
                    living_side_time[i - 1] = (random.randint(50, 100) / 10, time.time())
                    living_side_vels[i - 1] = (living_side_vels[i] + (random.randint(-5, 5) / 30))
                    if living_side_vels[i - 1] > .2:
                        living_side_vels[i - 1] = .2
                    if living_side_vels[i - 1] < -.2:
                        living_side_vels[i - 1] = -.2
            else:
                living_side_vels.append(.01)
                living_side_time.append((random.randint(30, 50) / 10, time.time()))
            plyr[i].change_side_vel(living_side_vels[i - 1])

        plyr[i].slow_side(angleY)

        if i != 0:
            preset = plyr[i].side_vel
            if plyr[i].collide(cube_place):
                plyr[i].collide_forward(angleY)
                chance = random.randint(1, 5)
                if chance != 5:
                    plyr[i].set_up_vel(-1.3)
                else:
                    living_forward_vels[i - 1] = -living_forward_vels[i - 1]
        else:
            # preset = plyr[i].side_vel
            # if plyr[i].collide(plot_cube_place):
            #     plyr[i].set_side_vel(0)
            #     plyr[i].move_side(.05, angleY)
            #     plyr[i].set_side_vel(0)
            #     if plyr[i].collide(plot_cube_place):
            #         plyr[i].set_side_vel(0)
            #         plyr[i].move_side(.05, angleY)
            #         plyr[i].set_side_vel(0)
            #         if plyr[i].collide(plot_cube_place):
            #             plyr[i].set_side_vel(0)
            #             plyr[i].move_side(.05, angleY)
            #             plyr[i].set_side_vel(0)
            #             if plyr[i].collide(plot_cube_place):
            #                 plyr[i].set_side_vel(0)
            #                 plyr[i].move_side(-.15, angleY)
            #                 plyr[i].set_side_vel(0)
            #                 if plyr[i].collide(plot_cube_place):
            #                     plyr[i].set_side_vel(0)
            #                     plyr[i].move_side(-.05, angleY)
            #                     plyr[i].set_side_vel(0)
            #                     if plyr[i].collide(plot_cube_place):
            #                         plyr[i].set_side_vel(0)
            #                         plyr[i].move_side(-.05, angleY)
            #                         plyr[i].set_side_vel(0)
            #                         if plyr[i].collide(plot_cube_place):
            #                             plyr[i].set_side_vel(0)
            #                             plyr[i].move_side(-.05, angleY)
            #                             plyr[i].set_side_vel(0)
            #                             if plyr[i].collide(plot_cube_place):
            #                                 plyr[i].set_side_vel(0)
            #                                 plyr[i].move_side(.15, angleY)
            #                                 plyr[i].set_side_vel(preset)
            #                                 plyr[i].collide_forward(angleY)
            if plyr[i].collide(plot_cube_place):
                plyr[i].collide_forward(angleY)

        if i == 0:
            if keys[pygame.K_w]:
                plyr[i].change_forward_vel(.2)
            if keys[pygame.K_s]:
                plyr[i].change_forward_vel(-.2)
        else:
            if len(living_forward_vels) > i:
                timer = living_forward_time[i - 1]
                if timer[1] < time.time() - timer[0]:
                    living_forward_time[i - 1] = (random.randint(50, 100) / 10, time.time())
                    living_forward_vels[i - 1] = (living_forward_vels[i - 1] + (random.randint(-5, 5) / 30))
                    if living_forward_vels[i - 1] > .2:
                        living_forward_vels[i - 1] = .2
                    if living_forward_vels[i - 1] < -.2:
                        living_forward_vels[i - 1] = -.2
            else:
                living_forward_vels.append(.01)
                living_forward_time.append((random.randint(30, 50) / 10, time.time()))
            plyr[i].change_forward_vel(living_forward_vels[i - 1])

        plyr[i].slow_forward(angleY)

        if i != 0:
            if plyr[i].collide(cube_place):
                plyr[i].collide_side(angleY)
                chance = random.randint(1, 5)
                if chance != 5:
                    plyr[i].set_up_vel(-1.3)
                else:
                    living_side_vels[i - 1] = -living_side_vels[i - 1]
        else:
            # preset = plyr[i].forward_vel
            # if plyr[i].collide(plot_cube_place):
            #     plyr[i].set_forward_vel(0)
            #     plyr[i].move_forward(.05, angleY)
            #     plyr[i].set_forward_vel(0)
            #     if plyr[i].collide(plot_cube_place):
            #         plyr[i].set_forward_vel(0)
            #         plyr[i].move_forward(.05, angleY)
            #         plyr[i].set_forward_vel(0)
            #         if plyr[i].collide(plot_cube_place):
            #             plyr[i].set_forward_vel(0)
            #             plyr[i].move_forward(.05, angleY)
            #             plyr[i].set_forward_vel(0)
            #             if plyr[i].collide(plot_cube_place):
            #                 plyr[i].set_forward_vel(0)
            #                 plyr[i].move_forward(-.15, angleY)
            #                 plyr[i].set_forward_vel(0)
            #                 if plyr[i].collide(plot_cube_place):
            #                     plyr[i].set_forward_vel(0)
            #                     plyr[i].move_forward(-.05, angleY)
            #                     plyr[i].set_forward_vel(0)
            #                     if plyr[i].collide(plot_cube_place):
            #                         plyr[i].set_forward_vel(0)
            #                         plyr[i].move_forward(-.05, angleY)
            #                         plyr[i].set_forward_vel(0)
            #                         if plyr[i].collide(plot_cube_place):
            #                             plyr[i].set_forward_vel(0)
            #                             plyr[i].move_forward(-.05, angleY)
            #                             plyr[i].set_forward_vel(0)
            #                             if plyr[i].collide(plot_cube_place):
            #                                 plyr[i].set_forward_vel(0)
            #                                 plyr[i].move_forward(.15, angleY)
            #                                 plyr[i].set_forward_vel(preset)
            #                                 plyr[i].collide_side(angleY)
            if plyr[i].collide(plot_cube_place):
                plyr[i].collide_side(angleY)

        plyr[i].move_up(.1)
        if plyr[i].collide(cube_place):
            plyr[i].collide_y()

        if plyr[i].collide(plot_cube_place, 1):
            if i == 0:
                if keys[pygame.K_SPACE]:
                    plyr[i].set_up_vel(-1.3)

        origin = plyr[i].get_origin()
        past_origin = (origin[0], origin[1], origin[2], player)
        if len(plot_cube_place) > i:
            plot_cube_place[i] = past_origin
        else:
            plot_cube_place.append(past_origin)

    origin = plot_cube_place[0]
    origin = tuple(origin)

    if keys[pygame.K_RIGHT]:
        # angleY += math.cos(angleZ) * .05
        # angleX += math.sin(angleZ) * .05
        # angleZ -= math.sin(angleX) * .05
        povX_dif -= .1

    if keys[pygame.K_LEFT]:
        # angleY -= math.cos(angleZ) * .05
        # angleX -= math.sin(angleZ) * .05
        # angleZ += math.sin(angleX) * .05
        povX_dif += .1
    povX = math.sin(povX_dif)
    povZ = math.cos(povX_dif)

    if keys[pygame.K_UP]:
        # angleZ -= math.sin(angleY) * .05
        # angleX += math.cos(angleY) * .05
        povY -= .1
    if keys[pygame.K_DOWN]:
        # angleZ += math.sin(angleY) * .05
        # angleX -= math.cos(angleY) * .05
        povY += .1

    if povY > -.05:
        povY = -.05
    if povY < -1.5:
        povY = -1.5

    # print(math.sin(povY*2))
    # angleX = math.sin(povY*2)
    angleX = 0
    angleY = math.atan2(povZ, povX) + 1.7

    if not first:
        if keys[pygame.K_y]:
            zoom += 10
        if keys[pygame.K_h]:
            zoom += -10
        if zoom > 800:
            zoom = 800
        if zoom < 10:
            zoom = 10

    if keys[pygame.K_u]:
        first_dif_zoom += 10
    if keys[pygame.K_j]:
        first_dif_zoom += -10

    if keys[pygame.K_1]:
        first = 1
    print(povY)
    if first:
        povY = -.25

    if keys[pygame.K_3]:
        first = 0
        zoom = 350

    if keys[pygame.K_r]:
        origin = (10, -20, 10)
        plyr[0].respawn()

    draw_map(cube_place, window, plyr, screen_w, plot_cube_place)
    plot_cube_place = close(cube_place, origin[0:3])

    if len(plot_cube_place) < 1:
        plot_cube_place.append((origin[0], origin[1], origin[2], player))
    else:
        plot_cube_place[0] = (origin[0], origin[1], origin[2], player)
    past_origin = (origin[0], origin[1], origin[2], player)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
pygame.quit()
