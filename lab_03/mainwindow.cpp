#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QColorDialog>
#include <QElapsedTimer>
#include <QStatusBar>
#include <cmath>


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow),
    fgColor(defaultFgColor),
    bgColor(defaultBgColor),
    scene(new QGraphicsScene(0, 0, 720, 720))
{
    ui->setupUi(this);
    ui->graphicsView->setScene(scene);
    clearImage();
    imageView();
    on_clearButton_clicked();
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

void MainWindow::imageView()
{
    scene->addPixmap(QPixmap::fromImage(image));
}

void MainWindow::on_colorLineButton_clicked()
{
    fgColor = QColorDialog::getColor(fgColor, this, "Pick a FG color", QColorDialog::DontUseNativeDialog);
    colorLabel(ui->fgLabel, fgColor);
}

void MainWindow::clearImage()
{
    image = QImage(721, 721, QImage::Format_ARGB32);
    image.fill(defaultBgColor);
    imageView();
}


void MainWindow::on_colorBackButton_clicked()
{
    bgColor = QColorDialog::getColor(bgColor, this, "Pick a BG color", QColorDialog::DontUseNativeDialog);
    image = QImage(721, 721, QImage::Format_ARGB32);
    image.fill(bgColor);
    imageView();
}


void MainWindow::on_clearButton_clicked()
{
    clearImage();
    imageView();
}


bool MainWindow::drawLine(const QLine &line, Canvas &canvas)
{
    if (ui->rbDDA->isChecked())
        return dda(line, canvas);
    else if (ui->rbBrezenhemFloat->isChecked())
        return bresenhamFloat(line, canvas);
    else if (ui->rbBrezenhemInt->isChecked())
        return bresenhamInteger(line, canvas);
    else if (ui->rbBrezenhemAntiLader->isChecked())
        return bresenhamAntialiased(line, canvas);
    else if (ui->rbStandart->isChecked())
        return defaultQt(line, canvas);
    else if (ui->rbWu->isChecked())
        return wu(line, canvas);
    return true;
}

void MainWindow::drawPoint(const QPoint &point)
{
    QPixmap pixmap = QPixmap::fromImage(image);
    QPainter painter(&pixmap);
    painter.setPen(Qt::red);

    painter.drawEllipse(point, 3, 3);

    painter.end();
    image = pixmap.toImage();
}


void MainWindow::on_lineDrawButton_clicked()
{
    const int x1 = 360 + ui->x1SpinBox->value();
    const int y1 = 360-ui->y1SpinBox->value();
    const int x2 = 360 + ui->x2SpinBox->value();
    const int y2 = 360-ui->y2SpinBox->value();
    const QLine line(x1, y1, x2, y2);

    Canvas canvas = { &image, &fgColor };

    QElapsedTimer timer;
    timer.start();

    drawLine(line, canvas);

    ui->statusbar->showMessage(QString::number(timer.nsecsElapsed() / 1000.0) + " μs");
    imageView();
}

static inline double toRadians(double x)
{
    return x * M_PI / 180;
}

void MainWindow::on_spectrDrawButton_clicked()
{
    int length = ui->lineSpinBox->value();
    int dangle = ui->angleSpinBox->value();
    if (dangle == 0 || length == 0)
    {
        ui->statusbar->showMessage("Введены не верные данные угла или длины линии спектра");
        return;
    }

    Canvas canvas = { &image, &fgColor };
    for (int angle = 0; angle < 360; angle += dangle)
    {
        const int x2 = 360 + round(length * cos(toRadians(angle)));
        const int y2 = 360 - round(length * sin(toRadians(angle)));
        if (!drawLine(QLine(360, 360, x2, y2), canvas))
            drawPoint(QPoint(x2, y2));
    }
    imageView();
}

