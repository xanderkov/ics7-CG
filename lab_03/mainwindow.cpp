#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QColorDialog>
#include <QElapsedTimer>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow),
    fgColor(defaultFgColor),
    scene(new QGraphicsScene(0, 0, 720, 720))
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::colorLabel(QLabel *label, QColor &color)
{
    QPalette palette = label->palette();
    palette.setColor(label->backgroundRole(), color);
    label->setAutoFillBackground(true);
    label->setPalette(palette);
}

void MainWindow::on_colorLineButton_clicked()
{
    fgColor = QColorDialog::getColor(fgColor, this, "Pick a FG color", QColorDialog::DontUseNativeDialog);
    colorLabel(ui->fgLabel, fgColor);
}

