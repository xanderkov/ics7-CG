from tkinter import *
from tkinter import messagebox
from tkinter import colorchooser
from math import radians, cos, sin, floor
import matplotlib.pyplot as plt
import time
from constants import *
from algorithms import *


# Получение параметров для отрисовки
def draw(test_mode):
    choise = method_list.curselection()
    if len(choise) == 1:
        xs, ys = fxs.get(), fys.get()
        xf, yf = fxf.get(), fyf.get()
        if not xs and not ys:
            messagebox.showwarning('Ошибка ввода',
                                   'Не заданы координаты начала отрезка!')
        elif not xs or not ys:
            messagebox.showwarning('Ошибка ввода',
                                   'Не задана одна из координат начала отрезка!')
        elif not xf and not yf:
            messagebox.showwarning('Ошибка ввода',
                                   'Не заданы координаты конца отрезка!')
        elif not xf or not yf:
            messagebox.showwarning('Ошибка ввода',
                                   'Не задана одна из координат конца отрезка!')
        else:
            # try:
            xs, ys = round(float(xs)), round(float(ys))
            xf, yf = round(float(xf)), round(float(yf))
            if xs != xf or ys != yf:
                if not test_mode:
                    if choise[0] == 5:
                        canvas.create_line([xs, ys], [xf, yf], fill=line_color)
                    else:
                        funcs[choise[0]](canvas, [xs, ys], [xf, yf], fill=line_color)
                else:
                    angle = fangle.get()
                    if angle:
                        try:
                            angle = int(angle)
                        except:
                            messagebox.showwarning('Ошибка ввода',
                                                   'Введено нечисловое значение для шага анализа!')
                        if angle:
                            if choise[0] != 5:
                                test(1, funcs[choise[0]], angle, [xs, ys], [xf, yf])
                            else:
                                standart_test(1, angle, [xs, ys], [xf, yf])
                        else:
                            messagebox.showwarning('Ошибка ввода',
                                                   'Задано нулевое значение для угла поворота!')

                    else:
                        messagebox.showwarning('Ошибка ввода',
                                               'Не задано значение для шага анализа!')
            else:
                messagebox.showwarning('Ошибка ввода',
                                       'Начало и конец отрезка совпадают!')
    elif not len(choise):
        messagebox.showwarning('Ошибка ввода',
                               'Не выбран метод построения отрезка!')
    else:
        messagebox.showwarning('Ошибка ввода',
                               'Выбрано более одного метода простроения отрезка!')


# Получение параметров для анализа
def analyze(mode):
    length = len_line.get()
    if length:
        length = int(length)
    else:
        length = 100
    if not mode:
        time_bar(length)
    else:
        ind = method_list.curselection()
        if ind:
            if ind[-1] != 5:
                smoth_analyze(ind, length)
            else:
                messagebox.showwarning('Предупреждение',
                                       'Стандартный метод не может '
                                       'быть проанализирован на ступенчатость!')
        else:
            messagebox.showwarning('Предупреждение',
                                   'Не выбрано ни одного'
                                   'метода построения отрезка!')


# замер времени
def test(flag, method, angle, pb, pe):
    global line_color
    total = 0
    steps = int(360 // angle)
    for i in range(steps):
        cur1 = time.time()
        if flag == 0:
            method(canvas, pb, pe, fill=bg_color)  # line_color)
        else:
            method(canvas, pb, pe, fill=line_color)
        cur2 = time.time()
        turn_point(radians(angle), pe, pb)
        total += cur2 - cur1
    return total / steps


def standart_test(flag, angle, pb, pe):
    global line_color
    total = 0
    steps = int(360 // angle)
    for i in range(steps):
        cur1 = time.time()
        if flag == 0:
            canvas.create_line(pb, pe, fill=bg_color)  # line_color)
        else:
            canvas.create_line(pb, pe, fill=line_color)
        cur2 = time.time()
        turn_point(radians(angle), pe, pb)
        total += cur2 - cur1
    return total / steps


# гистограмма времени
def time_bar(length):
    close_plt()
    plt.figure(2, figsize=(9, 7))
    times = []
    angle = 1
    pb = [center[0], center[1]]
    pe = [center[0] + 100, center[1]]
    for i in range(5):
        times.append(test(0, funcs[i], angle, pb, pe))
    clean()
    Y = range(len(times))

    L = ('Цифровой\nдифференциальный\nанализатор', 'Брезенхем\n(вещественные)',
             'Брезенхем\n(целые)', 'Брезенхем\n(с устранением\nступенчатости)', 'ВУ')
    plt.bar(Y, times, align='center')
    plt.xticks(Y, L)
    plt.ylabel("Время в секундах. (длина линии "+ str(length) + ")")
    plt.show()


# Поворот точки для сравнения ступенчатости
def turn_point(angle, p, center):
    x = p[0]
    p[0] = round(center[0] + (x - center[0]) * cos(angle) + (p[1] - center[1]) * sin(angle))
    p[1] = round(center[1] - (x - center[0]) * sin(angle) + (p[1] - center[1]) * cos(angle))


# Анализ ступечатости
def smoth_analyze(methods, length):
    close_plt()
    names = ('Цифровой\nдифференциальный\nанализатор', 'Брезенхем\n(вещественные)',
             'Брезенхем\n(целые)', 'Брезенхем\n(с устранением\nступенчатости)', 'ВУ')
    plt.figure(1)
    plt.title("Анализ ступенчатости")
    plt.xlabel("Угол")
    plt.ylabel("Номер шага (длина линии " + str(length) + ")")
    plt.grid(True)
    for i in methods:
        max_len = []
        nums = []
        angles = []
        angle = 0
        step = 2
        pb = [center[0], center[1]]
        pe = [center[0] + length, center[1]]

        for j in range(90 // step):
            stairs = funcs[i](canvas, pb, pe, line_color)
            turn_point(radians(step), pe, pb)
            if stairs:
                max_len.append(max(stairs))
            else:
                max_len.append(0)
            nums.append(len(stairs))
            angles.append(angle)
            angle += step
        clean()
        plt.figure(1)
        plt.plot(angles, nums, label=names[i])
        plt.legend()
    plt.show()


# Оси координат
def draw_axes():
    color = 'gray'
    canvas.create_line(0, 3, canvW, 3, width=1, fill='light gray', arrow=LAST)
    canvas.create_line(3, 0, 3, canvH, width=1, fill='light gray', arrow=LAST)
    for i in range(50, canvW, 50):
        canvas.create_text(i, 15, text=str(abs(i)), fill=color)
        canvas.create_line(i, 0, i, 5, fill=color)

    for i in range(50, canvH, 50):
        canvas.create_text(20, i, text=str(abs(i)), fill=color)
        canvas.create_line(0, i, 5, i, fill=color)


# очистка канваса
def clean():
    canvas.delete("all")
    draw_axes()



# Список методов прорисовки отрезка
def fill_list(lst):
    lst.insert(END, "Цифровой дифференциальный анализатор")
    lst.insert(END, "Брезенхем (float)")
    lst.insert(END, "Брезенхем (int)")
    lst.insert(END, "Брезенхем с устранением ступенчатости")
    lst.insert(END, "Ву")
    lst.insert(END, "Стандартный")


def get_color_bg():
    color_code = colorchooser.askcolor(title="Choose color")
    set_bgcolor(color_code[-1])


def get_color_line():
    color_code = colorchooser.askcolor(title="Choose color")
    set_linecolor(color_code[-1])


def set_bgcolor(color):
    global bg_color
    bg_color = color
    canvas.configure(bg=bg_color)


def set_linecolor(color):
    global line_color
    line_color = color
    lb_lcolor.configure(bg=line_color)


def close_plt():
    plt.figure(1)
    plt.close()
    plt.figure(2)
    plt.close()


def close_all():
    if messagebox.askyesno("Выход", "Вы действительно хотите завершить программу?"):
        close_plt()
        root.destroy()


root = Tk()
root.geometry('1366x700')
root.resizable(0, 0)
root.title('Лабораторная работа №3')
color_menu = "white"

# коэффициенты для линии
coords_frame = Frame(root, bg=color_menu, height=250, width=w_menu)
coords_frame.place(x=0, y=110)

# угол
angle_frame = Frame(root, bg=color_menu, height=250, width=w_menu)
angle_frame.place(x=0, y=250)

# выбор цвета
color_frame = Frame(root, bg=color_menu, height=150, width=w_menu)
color_frame.place(x=0, y=350)

# сравнение
comparison_frame = Frame(root, bg=color_menu, height=200, width=w_menu)
comparison_frame.place(x=0, y=500)

# очистить
menu_frame = Frame(root, bg=color_menu, height=50, width=w_menu)
menu_frame.place(x=0, y=600)

canvas = Canvas(root, width=canvW, height=canvH, bg='white')
canvas.place(x=w_menu, y=000)
center = (375, 200)

# Список Алгоритмов
method_list = Listbox(root, selectmode=EXTENDED)
method_list.place(x=0, y=1, width=w_menu, height=110)
fill_list(method_list)
funcs = (draw_line_cda, draw_line_brez_float, draw_line_brez_int,
         draw_line_brez_smoth, draw_line_vu, canvas.create_line)

lb1 = Label(coords_frame, bg=color_menu, text='Начало отрезка:')
lb2 = Label(coords_frame, bg=color_menu, text='Конец отрезка:')
lb1.place(x=0, y=5)
lb2.place(x=0, y=50)

lbx1 = Label(coords_frame, bg=color_menu, text='X:')
lby1 = Label(coords_frame, bg=color_menu, text='Y:')
lbx2 = Label(coords_frame, bg=color_menu, text='X:')
lby2 = Label(coords_frame, bg=color_menu, text='Y:')
lbx1.place(x=5, y=25)
lby1.place(x=95, y=25)
lbx2.place(x=5, y=75)
lby2.place(x=95, y=75)

fxs = Entry(coords_frame, bg="white")
fys = Entry(coords_frame, bg="white")
fxf = Entry(coords_frame, bg="white")
fyf = Entry(coords_frame, bg="white")
fxs.place(x=30, y=25, width=60)
fys.place(x=115, y=25, width=60)
fxf.place(x=30, y=75, width=60)
fyf.place(x=115, y=75, width=60)
fxs.insert(0, str(canvW / 2))
fys.insert(0, str(canvH / 2))
fxf.insert(0, 5)
fyf.insert(0, 5)

btn_draw = Button(coords_frame, text="Построить Линию", command=lambda: draw(0))
btn_draw.place(x=3, y=105, width=120, height=30)

lb_angle = Label(angle_frame, bg=color_menu, text="Угол поворота (в градусах):")
lb_angle.place(x=2, y=2)

fangle = Entry(angle_frame, bg="white")
fangle.place(x=180, y=2, width=60)
fangle.insert(0, "15")

btn_viz = Button(angle_frame, text="Построить Спектр", command=lambda: draw(1))
btn_viz.place(x=3, y=70, width=120, height=25)

lb_len = Label(angle_frame, bg=color_menu, text="Длина линии: ")
lb_len.place(x=30, y=40)
len_line = Entry(angle_frame, bg="white")
len_line.place(x=180, y=40, width=60)
len_line.insert(0, "100")
btn_time = Button(comparison_frame, text="Сравнение времени построения", command=lambda: analyze(0))
btn_time.place(x=3, y=0, width=250, height=25)
btn_smoth = Button(comparison_frame, text="Сравнение ступенчатости", command=lambda: analyze(1))
btn_smoth.place(x=3, y=30, width=250, height=25)

btn_clean = Button(menu_frame, text="Очистить экран", command=clean)
btn_clean.place(x=3, y=0, width=250)
# btn_exit = Button(menu_frame, text=u"Выход", command=close_all)
# btn_exit.place(x=60, y=0, width=95)


### --------------- выбор цветов ---------------
size = 15
white_line = Button(color_frame, bg="white", activebackground="white", highlightcolor="white",
                    command=lambda: set_linecolor('white'))
white_line.place(x=15, y=30, height=size, width=size)
black_line = Button(color_frame, bg="yellow", activebackground="yellow", highlightcolor="yellow",
                    command=lambda: set_linecolor("yellow"))
black_line.place(x=30, y=30, height=size, width=size)
red_line = Button(color_frame, bg="orange", activebackground="orange", highlightcolor="orange",
                  command=lambda: set_linecolor("orange"))
red_line.place(x=45, y=30, height=size, width=size)
orange_line = Button(color_frame, bg="red", activebackground="red",
                     command=lambda: set_linecolor("red"))
orange_line.place(x=60, y=30, height=size, width=size)
yellow_line = Button(color_frame, bg="purple", activebackground="purple",
                     command=lambda: set_linecolor("purple"))
yellow_line.place(x=75, y=30, height=size, width=size)
green_line = Button(color_frame, bg="darkblue", activebackground="darkblue",
                    command=lambda: set_linecolor("darkblue"))
green_line.place(x=90, y=30, height=size, width=size)
doger_line = Button(color_frame, bg="darkgreen", activebackground="darkgreen",
                    command=lambda: set_linecolor("darkgreen"))
doger_line.place(x=105, y=30, height=size, width=size)
blue_line = Button(color_frame, bg="black", activebackground="black",
                   command=lambda: set_linecolor("black"))
blue_line.place(x=120, y=30, height=size, width=size)

white_bg = Button(color_frame, bg="white", activebackground="white",
                  command=lambda: set_bgcolor("white"))
white_bg.place(x=15, y=110, height=size, width=size)
black_bg = Button(color_frame, bg="yellow", activebackground="yellow",
                  command=lambda: set_bgcolor("yellow"))
black_bg.place(x=30, y=110, height=size, width=size)
red_bg = Button(color_frame, bg="orange", activebackground="orange",
                command=lambda: set_bgcolor("orange"))
red_bg.place(x=45, y=110, height=size, width=size)
orange_bg = Button(color_frame, bg="red", activebackground="red",
                   command=lambda: set_bgcolor("red"))
orange_bg.place(x=60, y=110, height=size, width=size)
yellow_bg = Button(color_frame, bg="purple", activebackground="purple",
                   command=lambda: set_bgcolor("purple"))
yellow_bg.place(x=75, y=110, height=size, width=size)
green_bg = Button(color_frame, bg="darkblue", activebackground="darkblue",
                  command=lambda: set_bgcolor("darkblue"))
green_bg.place(x=90, y=110, height=size, width=size)
dodger_bg = Button(color_frame, bg="darkgreen", activebackground="darkgreen",
                   command=lambda: set_bgcolor("darkgreen"))
dodger_bg.place(x=105, y=110, height=size, width=size)
blue_bg = Button(color_frame, bg="black", activebackground="black",
                 command=lambda: set_bgcolor("black"))
blue_bg.place(x=120, y=110, height=size, width=size)


lb_line = Button(color_frame, bg=color_menu, text='Цвет линии (текущий:): ', command=get_color_line)
lb_line.place(x=2, y=5, width=170)
lb_lcolor = Label(color_frame, bg=line_color)
lb_lcolor.place(x=160, y=13, width=12, height=12)
lb_bg = Button(color_frame, bg=color_menu, text='Цвет фона: ', command=get_color_bg)
lb_bg.place(x=2, y=80)

draw_axes()
root.mainloop()
