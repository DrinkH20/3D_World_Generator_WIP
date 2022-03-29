import math
import perlin_noise
import random

noise = perlin_noise.PerlinNoise()
# fav is .009

noise_scale = .01

running = True

screen_w, screen_h = 50, 50

# Place has x, y, and z
place = []
draw = []
dots = []

grass = (100, 165, 100)
rock = (100, 100, 100)
wood = (165, 165, 100)


def generate_tree(x, y, gz):
    place.append((x, y - 2, gz, wood))
    place.append((x, y - 4, gz, wood))
    place.append((x - 2, y - 6, gz, grass))
    place.append((x + 2, y - 6, gz, grass))
    place.append((x, y - 6, gz - 2, grass))
    place.append((x, y - 6, gz + 2, grass))
    place.append((x, y - 8, gz, grass))


def fill():
    for x in range(int(screen_w/1)):
        for z in range(int(screen_h/1)):
            pre_num = noise.noise((x * noise_scale, z * noise_scale))
            n = round(pre_num * 100)*2
# place.append((round(x*2)/2, round(z*2)/2, round(n*2)/2, (100, 100, 100)))
# if not place.__contains__((round(x / 2) * 2, round(n / 2) * 2, round(z / 2) * 2, (100, 100, 100))):
#     if not place.__contains__((round(x / 2) * 2, round(n / 2) * 2, round(z / 2) * 2, (100, 130, 100))):
#         if not place.__contains__((round(x / 2) * 2, round(n / 2) * 2, round(z / 2) * 2, (100, 150, 100))):
#             if n < -6:
#                 place.append((round(x / 2) * 2, round(n / 2) * 2, round(z / 2) * 2, (100, 100, 100)))
#             elif n < 3:
#                 place.append((round(x / 2) * 2, round(n / 2) * 2, round(z / 2) * 2, (100, 130, 100)))
#                 ran = random.randint(1, 100)
#                 if ran == 1:
#                     generate_tree(round(x / 2) * 2, round(n / 2) * 2, round(z / 2) * 2)
#             else:
#                 place.append((round(x / 2) * 2, round(n / 2) * 2, round(z / 2) * 2, (100, 150, 100)))
#                 ran = random.randint(1, 50)
#                 if ran == 1:
#                     generate_tree(round(x / 2) * 2, round(n / 2) * 2, round(z / 2) * 2)
            if n < -6:
                place.append((x * 2, round(n / 2) * 2, z * 2, (100, 100, 100)))
            elif n < 3:
                place.append((x * 2, round(n / 2) * 2, z * 2, (100, 130, 100)))
                ran = random.randint(1, 250)
                if ran == 11:
                    generate_tree(x * 2, round(n / 2) * 2, z * 2)
            elif n < 30:
                place.append((x * 2, round(n / 2) * 2, z * 2, (100, 150, 100)))
                ran = random.randint(1, 200)
                if ran == 11:
                    generate_tree(x * 2, round(n / 2) * 2, z * 2)
                    # dots.append(((10, 50, 100 * abs(pre_num)), (x * 4, z * 4), 3))
            else:
                place.append((x * 2, 30, z * 2, (100, 100, 150)))

    return place


def close(lis, origin):
    global draw
    draw = []
    for m in lis:
        # Not adding the y difference because it makes it kind strange
        dist = (m[0]-origin[0])**2 + (m[2]-origin[2])**2
        if math.sqrt(abs(dist)) < 15:
            draw.append(m)

    return draw


fill()
# s = 0
# e = len(dots) - 1
# place = quicksort(place, s, e, 2)
#
# while running:
#     window.fill((143, 196, 204))
#     dots = []
#     place = []
#     fill()
#     print(dots)
#     draw = close(dots)
#
#     for i in draw:
#         pygame.draw.circle(window, i[0], i[1], i[2])
#     origin[0] += 20
#     origin[1] += 20
#     pygame.display.update()
