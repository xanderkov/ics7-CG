from turtle import distance
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPen, QImage, QPixmap, QPainter, QPolygon
from PyQt5.QtCore import Qt, QPoint
from kb_cut import *
import sys
from copy import deepcopy
from math import sqrt

global w


# код цвета по названию
def find_color_code(color_name):
    if color_name == 'Красный':
        return Qt.red
    elif color_name == 'Зеленый':
        return Qt.green
    elif color_name == 'Синий':
        return Qt.darkBlue
    elif color_name == 'Желтый':
        return Qt.yellow
    elif color_name == 'Голубой':
        return Qt.blue
    elif color_name == 'Бирюзовый':
        return Qt.cyan
    elif color_name == 'Розовый':
        return Qt.magenta
    elif color_name == 'Черный':
        return Qt.black


# для добаления точки по нажатию мышкой
class myScene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        point = [round(event.scenePos().x()), round(event.scenePos().y())]
        if event.buttons() == Qt.LeftButton:
            w.add_segment_point(point)
        if event.buttons() == Qt.RightButton:
            w.add_cutter_point(point)


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # для доступа к переменным, методам и т.д. в файле design.py
        super().__init__()
        # инициализация дизайна
        uic.loadUi("design.ui", self)
        # настройка кнопок
        self.but_clean.clicked.connect(self.on_bt_clean_clicked)
        self.but_connect.clicked.connect(self.on_bt_connect_clicked)
        self.but_input_point_cutter.clicked.connect(self.on_bt_input_point_cutter_clicked)
        self.but_input_point_segment.clicked.connect(self.on_bt_input_point_segment_clicked)
        self.but_cut.clicked.connect(self.on_bt_cut_clicked)
        self.but_parallel.clicked.connect(self.on_bt_parallel_clicked)
        
        self.color_back = Qt.white
        self.color_cutter = None
        self.color_segment = None
        self.color_result = None

        self.cutter_points = []
        self.direction = 0
        self.segments = []
        self.segment_prev = None

        # создание сцены
        self.scene = myScene(0, 0, 760, 660)
        self.scene.win = self
        self.graph.setScene(self.scene)
        # изображение
        self.image = QImage(760, 660, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(self.color_back)

    # обработка ошибки
    def handle_error(self, title, error):
        em = QtWidgets.QMessageBox(self.centralwidget)
        em.setText(error)
        em.setWindowTitle(title)
        em.exec()

    # очистка экрана и данных
    def on_bt_clean_clicked(self):
        self.scene.clear()
        self.image.fill(self.color_back)

        for i in range(self.table_cutter.rowCount(), -1, -1):
            self.table_cutter.removeRow(i)
        self.table_cutter.clearContents()

        for i in range(self.table_segments.rowCount(), -1, -1):
            self.table_segments.removeRow(i)
        self.table_segments.clearContents()

        self.color_back = Qt.white
        self.color_cutter = None
        self.color_segment = None
        self.color_result = None

        self.cutter_points = []
        self.segments = []
        self.segment_prev = None
        self.direction = 0
        
    def find_parallel(self, x1, y1, x2, y2):
        distance = 20
        ratio = 1.5
        dx = x2 - x1
        dy = y2 - y1
        len = sqrt(dx*dx+dy*dy)
        udx = dx / len
        udy = dy / len 
        perpx = -udy * distance
        perpy = udx * distance

        # "left" line start
        x1_ = x1 + perpx
        y1_ = y1 + perpy
        # "left" line end
        x2_ = x1_ + dx * ratio
        y2_ = y1_ + dy * ratio
        return x1_, y1_, x2_, y2_
    
    
    def on_bt_parallel_clicked(self):
        num = self.table_cutter.currentRow()
        if (num == -1):
            self.handle_error('Ошибка.', 'Не выбрана сторона отсекателя в таблице')
            return;
    
        x1 = int(self.table_cutter.item(num, 0).text())
        y1 = int(self.table_cutter.item(num, 1).text())
        print(num)
        num += 1
        
        if (num == self.table_cutter.rowCount()):
            num = 1
        
        x2 = int(self.table_cutter.item(num, 0).text())
        y2 = int(self.table_cutter.item(num, 1).text())
        if (x1 == x2 and y2 == y1):
            num += 1
            x2 = int(self.table_cutter.item(num, 0).text())
            y2 = int(self.table_cutter.item(num, 1).text())
        x1_, y1_, x2_, y2_ = self.find_parallel(x1, y1, x2, y2)
        self.add_segment_point([x1_, y1_])
        self.add_segment_point([x2_, y2_])
        segment = [x1_, y1_, x2_, y2_, self.color_segment]
        self.draw_segments([segment])
        
        

    # добавление строки в таблицу
    def add_row_to_table_cutter(self):
        self.table_cutter.insertRow(self.table_cutter.rowCount())

    def add_row_to_table_segments(self):
        self.table_segments.insertRow(self.table_segments.rowCount())

    # настройка цвета отсекателя
    def get_color_cutter(self):
        color_name = self.box_color_cutter.currentText()
        color_code = find_color_code(color_name)
        self.color_cutter = color_code

    # настройка цвета отрезков
    def get_color_segment(self):
        color_name = self.box_color_segment.currentText()
        color_code = find_color_code(color_name)
        self.color_segment = color_code

    # настройка цвета результата
    def get_color_result(self):
        color_name = self.box_color_result.currentText()
        color_code = find_color_code(color_name)
        self.color_result = color_code

    # общий алгоритм добавления вершины отрезка
    def add_segment_point(self, point):
        self.get_color_segment()
        if not self.segment_prev:
            self.draw_segments([[point[0], point[1], point[0], point[1], self.color_segment]])
            self.segment_prev = point
            # добавление в таблицу
            
        else:
            self.draw_segments([[self.segment_prev[0], self.segment_prev[1], point[0], point[1], self.color_segment]])
            self.segments.append([self.segment_prev[0], self.segment_prev[1], point[0], point[1], self.color_segment])
            # добавление в таблицу
            self.segment_prev = None

    # добавление вершины отрезка по кнопке
    def on_bt_input_point_segment_clicked(self):
        self.add_segment_point([self.box_x.value(), self.box_y.value()])

    # отрисовка исходных отрезков
    def draw_segments(self, segments):
        p = QPainter()
        p.begin(self.image)
        for segment in segments:
            p.setPen(QPen(segment[-1]))
            self.my_darw_line(p, segment[:-1])
        p.end()

        pix = QPixmap()  # отрисовываемая картинка
        pix.convertFromImage(self.image)
        self.scene.addPixmap(pix)

    # отрисовка отсекателя
    def draw_cutter(self):
        p = QPainter()
        p.begin(self.image)
        self.get_color_cutter()
        p.setPen(QPen(self.color_cutter))
        for i in range(len(self.cutter_points) - 1):
            segment = [self.cutter_points[i][0], self.cutter_points[i][1],
                       self.cutter_points[i + 1][0], self.cutter_points[i + 1][1]]
            self.my_darw_line(p, segment)

        if len(self.cutter_points) == 1:
            segment = [self.cutter_points[0][0], self.cutter_points[0][1],
                       self.cutter_points[0][0], self.cutter_points[0][1]]
            self.my_darw_line(p, segment)
        p.end()

        pix = QPixmap()  # отрисовываемая картинка
        pix.convertFromImage(self.image)
        self.scene.addPixmap(pix)

    # добавление вершины отcекателя по кнопке
    def on_bt_input_point_cutter_clicked(self):
        self.add_cutter_point([self.box_x.value(), self.box_y.value()])

    # добавление вершины отсекателя
    def add_cutter_point(self, point):
        cur_direction = 0
        if len(self.cutter_points) > 1:
            cur_direction = vect_mult_sign_z(self.cutter_points[-2], self.cutter_points[-1], point)
            if self.direction == 0:
                self.direction = cur_direction

        if (self.direction != cur_direction) and (self.direction != 0) and (cur_direction != 0):
            self.handle_error('Ошибка.', 'Отсекатель должен быть выпуклым многоугольником')
            return

        self.cutter_points.append(point)
        self.draw_cutter()
        # добавление в таблицу
        i = self.table_cutter.rowCount()
        self.add_row_to_table_cutter()
        x = QTableWidgetItem("{}".format(point[0]))
        y = QTableWidgetItem("{}".format(point[1]))
        self.table_cutter.setItem(i, 0, x)
        self.table_cutter.setItem(i, 1, y)

    # замыкание контура отсекателя
    def on_bt_connect_clicked(self):
        if not self.cutter_points:
            self.handle_error("Ошибка", "Не было введено ни одной точки отсекателя")
        else:
            self.add_cutter_point(self.cutter_points[0])

    def my_repaint(self):
        self.image.fill(self.color_back)
        self.draw_segments(self.segments)
        self.draw_cutter()

    def my_help(self, p):
        a = QPolygon()
        for point in self.cutter_points:
            new_point = QPoint(point[0], point[1])
            a.append(new_point)
        p.setPen(QPen(self.color_cutter, 1))
        p.setBrush(self.color_back)
        p.drawPolygon(a, 1)

    # рисование отрезка
    def my_darw_line(self, p, segment):
        p.drawLine(*segment)
        # points = bresenham_int(*segment)
        # for point in points:
        #     p.drawPoint(*point)

    # отсечение
    def on_bt_cut_clicked(self):
        if not self.cutter_points:
            self.handle_error("Ошибка", "Сначала введите отсекатель")
            return
        if (self.cutter_points[0][0] != self.cutter_points[-1][0]) or \
            (self.cutter_points[0][1] != self.cutter_points[-1][1]):
            self.handle_error("Ошибка", "Отсекатель не замкнут")
            return

        width = self.box_width.value()
        self.get_color_result()

        if self.segment_prev:
            self.segments.append([self.segment_prev[0], self.segment_prev[1],
                                 self.segment_prev[0], self.segment_prev[1], self.color_segment])

        self.my_repaint()
        p = QPainter()
        p.begin(self.image)
        p.setPen(QPen(self.color_result, width))
        flag = 1
        for segment in self.segments:
            p1 = [segment[0], segment[1]]
            p2 = [segment[2], segment[3]]
            rc, segment_cut = kb_cut(p1, p2, len(self.cutter_points), deepcopy(self.cutter_points))
            if rc == OK:
                if flag:
                    self.my_help(p)
                    p.setPen(QPen(self.color_result, width))
                    flag = 0
                if segment_cut:
                    self.my_darw_line(p, segment_cut)
            else:
                if rc == ERR_DEG:
                    self.handle_error("Ошибка", "Отсекатель вырожден")
                    return
                elif rc == ERR_CONV:
                    self.handle_error("Ошибка", "Отсекатель должен быть выпуклым многоугольником")
                    return

        p.end()
        pix = QPixmap()  # отрисовываемая картинка
        pix.convertFromImage(self.image)
        self.scene.addPixmap(pix)
        
    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    w = MyWindow()  # Создаём объект класса ExampleApp
    w.show()  # Показываем окно
    sys.exit(app.exec_())  # и запускаем приложение
