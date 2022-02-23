#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QGraphicsView>
#include <QLineEdit>
#include <QPainter>
#include <QPainterPath>
#include <QGraphicsPathItem>

#include "geometry.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();


private slots:
    void on_pushButtonTransfer_clicked();

    void on_pushButtonScale_clicked();

    void on_pushButtonTurn_clicked();

    void on_pushButtonBack_clicked();

    bool get_var(double &var, const QLineEdit *lineEdit, const QString &err_msg);

    void on_checkBox_stateChanged(int arg1);

    void on_pushButtonOriginal_clicked();


private:
    void initPoints();
    double x_coord(double x) const;
    double y_coord(double y) const;
    QPointF coord(const Point &point) const;
    double anti_coord_x(double x) const;
    double anti_coord_y(double y) const;
    QPen choosePen(int i) const;

private:
    Ui::MainWindow *ui;
    QGraphicsScene *scene;

    void drawOriginalImage();

    double x_max = 0, y_max = 0, x_min = 0, y_min = 0, maxRect, minRect;
    static const int PAINT_WIDTH = 600;
    static const int PAINT_HEIGHT = 600;
    double scale_factor;

    static const int STATUS_BAR_TIMEOUT = 5000;
    static const int NORMAL_SCALE_FACTOR = 25;
    static const int COMPRESS_MIN = (2.0 * NORMAL_SCALE_FACTOR) / PAINT_HEIGHT;
    double compress = 1;
    bool autoscaling = 0;

    double a = 3;
    double b = 3;

    double x, y;
    double kx, ky;
    double alpha;

    int n = 1000;

    QVector<Point> points;
    QVector<Transform> transforms;
};
#endif // MAINWINDOW_H
