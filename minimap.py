import math
import pygame

# from ThreeD import *


def draw_map(li, win, playr, scrw, plot):
    dif = scrw/len(li)*100
    # print(int(math.sqrt(len(li))/10), "divide")
    divide = int(math.sqrt(len(li))/10)
    for pl in range(round(len(li)/divide)):
        piece = li[pl*divide]
        pygame.draw.circle(win, piece[3], (piece[0]*dif, -piece[2]*dif + 100), 7)

    for piece in range(len(playr)):
        if piece == 0:
            objct = plot[piece]
            pygame.draw.circle(win, (255, 255, 255), (objct[0] * dif, -objct[2] * dif + 100), 2)
        else:
            objct = plot[piece]
            pygame.draw.circle(win, (255, 150, 150), (objct[0] * dif, -objct[2] * dif + 100), 2)
