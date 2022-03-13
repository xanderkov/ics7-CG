#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QLabel>
#include <QGraphicsScene>

#include "canvas.h"
#include "algorithms.h"
#include <QMessageBox>

#define HEIGHT 650
#define WIDTH 1100

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    void colorLabel(QLabel *label, QColor &color);
    void clearImage();
    void imageView();
    bool drawLine(const QLine &line, Canvas &canvas);
    void drawPoint(const QPoint &point);

private slots:
    void on_colorLineButton_clicked();

    void on_colorBackButton_clicked();

    void on_clearButton_clicked();

    void on_lineDrawButton_clicked();

    void on_spectrDrawButton_clicked();

    void on_calcTimeButton_clicked();

    void on_compareLadderButton_clicked();

private:
    Ui::MainWindow *ui;

    QColor fgColor;
    QColor bgColor;
    const QColor defaultBgColor = QColor(11, 11, 11);
    const QColor defaultFgColor = QColor(255, 255, 255);
    QImage image;
    QGraphicsScene *scene;
};
#endif // MAINWINDOW_H
