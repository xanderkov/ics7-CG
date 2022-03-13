from calculations import sign, get_rgb_intensity
from tkinter import *
from math import radians, cos, sin, floor
from constants import *


def draw_line_brez_smoth(canvas, ps, pf, fill):
    I = 100
    fill = get_rgb_intensity(canvas, fill, bg_color, I)
    dx = pf[0] - ps[0]
    dy = pf[1] - ps[1]
    sx = sign(dx)
    sy = sign(dy)
    dy = abs(dy)
    dx = abs(dx)
    if dy >= dx:
        dx, dy = dy, dx
        steep = 1  #
    else:
        steep = 0  #
    tg = dy / dx * I  # тангенс угла наклона (умножаем на инт., чтобы не приходилось умножать внутри цикла
    e = I / 2  # интенсивность для высвечивания начального пикселя
    w = I - tg  # пороговое значение
    x = ps[0]
    y = ps[1]
    stairs = []
    st = 1
    while x != pf[0] or y != pf[1]:
        if e < w:
            if steep == 0:  # dy < dx
                x += sx  # -1 if dx < 0, 0 if dx = 0, 1 if dx > 0
            else:  # dy >= dx
                y += sy  # -1 if dy < 0, 0 if dy = 0, 1 if dy > 0
            st += 1  # stepping
            e += tg
        elif e >= w:
            x += sx
            y += sy
            e -= w
            stairs.append(st)
            st = 0
    if st:
        stairs.append(st)
    return stairs


def draw_line_cda(canvas, ps, pf, fill):
    dx = abs(pf[0] - ps[0])
    dy = abs(pf[1] - ps[1])

    # for stairs counting
    if dx:
        tg = dy / dx
    else:
        tg = 0

    # steep - max growth
    if dx > dy:
        steep = dx
    else:
        steep = dy
    sx = (pf[0] - ps[0]) / steep  # step of x
    sy = (pf[1] - ps[1]) / steep  # step of y

    # set line to start
    x = ps[0]
    y = ps[1]
    stairs = []
    st = 1
    while abs(x - pf[0]) > 1 or abs(y - pf[1]) > 1:
        if (abs(int(x) - int(x + sx)) >= 1 and tg > 1) or (abs(int(y) - int(y + sy)) >= 1 >= tg):
            stairs.append(st)
            st = 0
        else:
            st += 1
        x += sx
        y += sy
    if st:
        stairs.append(st)
    return stairs


def draw_line_vu(canvas, ps, pf, fill):
    x1 = ps[0]
    x2 = pf[0]
    y1 = ps[1]
    y2 = pf[1]
    I = 100
    stairs = []
    fills = get_rgb_intensity(canvas, fill, bg_color, I)

    steep = abs(y2 - y1) > abs(x2 - x1)

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        tg = 1
    else:
        tg = dy / dx

    # first endpoint
    xend = round(x1)
    yend = y1 + tg * (xend - x1)
    xpx1 = xend
    y = yend + tg

    # second endpoint
    xend = int(x2 + 0.5)
    xpx2 = xend
    st = 0

    # main loop
    if steep:
        for x in range(xpx1, xpx2):

            if (abs(int(x) - int(x + 1)) >= 1 and tg > 1) or \
                    (not 1 > abs(int(y) - int(y + tg)) >= tg):
                stairs.append(st)
                st = 0
            else:
                st += 1
            y += tg
    else:
        for x in range(xpx1, xpx2):
            if (abs(int(x) - int(x + 1)) >= 1 and tg > 1) or \
                    (not 1 > abs(int(y) - int(y + tg)) >= tg):
                stairs.append(st)
                st = 0
            else:
                st += 1
            y += tg
    return stairs


# Брезенхема с действительными коэффами
def draw_line_brez_float(canvas, ps, pf, fill):
    dx = pf[0] - ps[0]
    dy = pf[1] - ps[1]
    sx = sign(dx)
    sy = sign(dy)
    dy = abs(dy)
    dx = abs(dx)

    if dy >= dx:
        dx, dy = dy, dx
        steep = 1  # шагаем по y
    else:
        steep = 0

    tg = dy / dx  # tангенс угла наклона
    e = tg - 1 / 2  # начальное значение ошибки
    x = ps[0]  # начальный икс
    y = ps[1]  # начальный игрек
    stairs = []
    st = 1
    while x != pf[0] or y != pf[1]:
        # выбираем пиксель
        if e >= 0:
            if steep == 1:  # dy >= dx
                x += sx
            else:  # dy < dx
                y += sy
            e -= 1  # отличие от целого
            stairs.append(st)
            st = 0
        if e <= 0:
            if steep == 0:  # dy < dx
                x += sx
            else:  # dy >= dx
                y += sy
            st += 1
            e += tg  # отличие от целого

    if st:
        stairs.append(st)
    return stairs


# Брезенхема с целыми коэффами
def draw_line_brez_int(canvas, ps, pf, fill):
    dx = pf[0] - ps[0]
    dy = pf[1] - ps[1]
    sx = sign(dx)
    sy = sign(dy)
    dy = abs(dy)
    dx = abs(dx)
    if dy >= dx:
        dx, dy = dy, dx
        steep = 1
    else:
        steep = 0
    e = 2 * dy - dx  # отличие от вещественного (e = tg - 1 / 2) tg = dy / dx
    x = ps[0]
    y = ps[1]
    stairs = []
    st = 1
    while x != pf[0] or y != pf[1]:
        if e >= 0:
            if steep == 1:
                x += sx
            else:
                y += sy
            stairs.append(st)
            st = 0
            e -= 2 * dx  # отличие от вещественного (e -= 1)
        if e <= 0:
            if steep == 0:
                x += sx
            else:
                y += sy
            st += 1
            e += 2 * dy  # difference (e += tg)

    if st:
        stairs.append(st)
    return stairs