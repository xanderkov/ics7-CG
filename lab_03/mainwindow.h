#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QLabel>
#include <QGraphicsScene>

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

private slots:
    void on_colorLineButton_clicked();

private:
    Ui::MainWindow *ui;

    QColor fgColor;
    const QColor defaultBgColor = QColor(11, 11, 11);
    const QColor defaultFgColor = QColor(10, 200, 10);

    QImage image;
    QGraphicsScene *scene;
};
#endif // MAINWINDOW_H
