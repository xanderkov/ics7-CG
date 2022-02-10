#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QVector>
#include <QTableWidgetItem>
#include <QLineEdit>
#include <QPainter>

#include <QPaintEvent>


#include "logic.h"

#define N 1000

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE



class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void paintEvent(QPaintEvent *event);

private slots:
    void on_addButton_clicked();

    void on_delButton_clicked();

    void on_tableWidget_cellChanged(int row, int column);

    void on_tableWidget_itemChanged(QTableWidgetItem *item);

    void on_calcButton_clicked();

private:



    bool get_var(double &var, const QLineEdit *lineEdit, const QString &err_msg);

    double x_coord(double x) const;
    double y_coord(double y) const;
    QPointF coord(const Point &point) const;
    void drawLine(const Line &line, QPainter &painter);
    QPen choosePen(int i) const;

private:
    Ui::MainWindow *ui;
    QVector<Point> points;
    int j_max = 0, i_max = 0, k_max = 0;
    double angle_min = 1000;
    Point incenterMax;
    Point rectCenter;
    double x_max = 0, y_max = 0, x_min = 0, y_min = 0, maxRect, minRect;
    double scale_factor;

    static const int STATUS_BAR_TIMEOUT = 10000;
    static const int PAINT_WIDTH = 600;
    static const int PAINT_HEIGHT = 500;
};
#endif // MAINWINDOW_H
