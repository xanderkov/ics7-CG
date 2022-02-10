#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

bool MainWindow::get_var(double &var, const QLineEdit *lineEdit, const QString &err_msg)
{
    bool ok;
    var = lineEdit->text().toDouble(&ok);
    if (!ok)
        ui->statusbar->showMessage(err_msg, STATUS_BAR_TIMEOUT);
    return ok;
}

void MainWindow::on_addButton_clicked()
{
    double x, y;
    if (!(get_var(x, ui->xCoordEdit, "Invalid x") && get_var(y, ui->yCoordEdit, "Invalid y")))
        return;
    Point point(x, y);
    j_max = 0;
    /*
    if (points.contains(point))
    {
        ui->statusbar->showMessage("Point already exists", STATUS_BAR_TIMEOUT);
        return;
    }
    */
    points.push_back(point);
    int i = ui->tableWidget->rowCount();
    ui->tableWidget->insertRow(i);
    ui->tableWidget->setItem(i, 0, new QTableWidgetItem(QString::number(x)));
    ui->tableWidget->setItem(i, 1, new QTableWidgetItem(QString::number(y)));

    ui->statusbar->showMessage("Point added successful", STATUS_BAR_TIMEOUT);
}


void MainWindow::on_delButton_clicked()
{
    bool ok;
    int i = ui->indexEdit->text().toInt(&ok);
    if (!ok)
    {
        ui->statusbar->showMessage("Invalid index", STATUS_BAR_TIMEOUT);
        return;
    }
    if (i <= 0 || i > points.size())
    {
        ui->statusbar->showMessage("Index out of range", STATUS_BAR_TIMEOUT);
        return;
    }

    j_max = 0;
    points.remove(i - 1);

    ui->tableWidget->removeRow(i - 1);

    ui->statusbar->showMessage("Point deleted successful", STATUS_BAR_TIMEOUT);
}


void MainWindow::on_tableWidget_cellChanged(int row, int column)
{
}


void MainWindow::on_tableWidget_itemChanged(QTableWidgetItem *item)
{
    bool ok;
    double coord = item->text().toDouble(&ok);
    if (!ok)
    {
        if (item->column())
            ui->statusbar->showMessage("Invalid y", STATUS_BAR_TIMEOUT);
        else
            ui->statusbar->showMessage("Invalid x", STATUS_BAR_TIMEOUT);
        item->setText(QString::number(points[item->row()][item->column()]));
        return;
    }

    Point point(coord, coord);
    point[!item->column()] = points[item->row()][!item->column()];

    j_max = 0;
    points[item->row()][item->column()] = coord;

    ui->statusbar->showMessage("Point edited successful", STATUS_BAR_TIMEOUT);
}


void MainWindow::on_calcButton_clicked()
{
    if (j_max)
    {
        ui->statusbar->showMessage("Already calculated", STATUS_BAR_TIMEOUT);
        return;
    }
    if (points.size() < 7)
    {
        ui->statusbar->showMessage("Too few points", STATUS_BAR_TIMEOUT);
        return;
    }
    int i, j, k;
    angle_min = 1000;
    Line y_axis(1, 0, 0);
    if (isRect(points[0], points[1], points[2], points[3]))
        rectCenter = Rectangle(points[0], points[1], points[2], points[3]).getRectCenter();
    else
    {
        ui->statusbar->showMessage("It is not rectangle", STATUS_BAR_TIMEOUT);
        return;
    }
    for (i = 4; i < points.size() - 2; ++i)
        for (j = i + 1; j < points.size() - 1; ++j)
            for (k = j + 1; k < points.size(); ++k)
                if (!on_one_line(points[i], points[j], points[k]))
                {
                    Point incenter = Triangle(points[i], points[j], points[k]).incenter();
                    double cur_angle = getAngle(Line(rectCenter, incenter));
                    if (cur_angle < angle_min)
                    {
                        i_max = i, j_max = j, k_max = k;
                        incenterMax = incenter;
                        angle_min = cur_angle;
                    }

                }

    if (!j_max)
    {
        ui->statusbar->showMessage("No one triangle can be drawn", STATUS_BAR_TIMEOUT);
        return;
    }

    ui->statusbar->showMessage(
        "Triangle found successful on points "
        + QString::number(i_max + 1) + ", "
        + QString::number(j_max + 1) + " and "
        + QString::number(k_max + 1) + ". Angle: "
        + QString::number(angle_min * 180 / 3.1415926)
    );
    update();
}


double MainWindow::x_coord(double x) const
{
    return PAINT_WIDTH / 2 + (x - x_min - 0.5 * (x_max - x_min)) * scale_factor;
}

double MainWindow::y_coord(double y) const
{
    return PAINT_HEIGHT / 2 - (y - y_min - 0.5 * (y_max - y_min)) * scale_factor;
}

QPointF MainWindow::coord(const Point &point) const
{
    return QPointF(x_coord(point.x), y_coord(point.y));
}

QPen MainWindow::choosePen(int i) const
{
    if (i % 50 == 0)
        return QPen(Qt::black);
    if (i % 10 == 0)
        return QPen(Qt::darkGray);
    if (i % 5 == 0)
        return QPen(Qt::gray);
    return QPen(Qt::lightGray);
}

void MainWindow::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    int w = ui->centralwidget->width() - ui->tableWidget->width() - 30, h =  ui->centralwidget->height() - 20;
    painter.translate(ui->tableWidget->width() + 30, 10);
    painter.fillRect(0, 0, w, h, Qt::white);

    if (!j_max)
        return;

    // find scale factor
    maxRect = qMax(qMax(points[0].x, qMax(points[1].x, points[3].x)), qMax(points[2].x, points[3].x));
    x_max = qMax(qMax(points[i_max].x, qMax(points[j_max].x, incenterMax.x)), qMax(points[k_max].x, incenterMax.x));
    x_max = qMax(maxRect, x_max);
    maxRect = qMax(qMax(points[0].y, qMax(points[1].y, points[3].y)), qMax(points[2].y, points[3].y));
    y_max = qMax(qMax(points[i_max].y, points[j_max].y), qMax(points[k_max].y, incenterMax.y));
    y_max = qMax(maxRect, y_max);
    minRect = qMin(qMin(points[0].x, qMin(points[1].x, points[3].x)), qMin(points[2].x, points[3].x));
    x_min = qMin(qMin(points[i_max].x, points[j_max].x), qMin(points[k_max].x, incenterMax.x));
    x_min = qMin(minRect, x_min);
    minRect = qMin(qMax(points[0].y, qMin(points[1].y, points[3].y)), qMin(points[2].y, points[3].y));
    y_min = qMin(qMin(points[i_max].y, points[j_max].y), qMin(points[k_max].y, incenterMax.y));
    y_min = qMin(minRect, y_min);
    double scale_x = 0.9 * PAINT_WIDTH / (x_max - x_min);
    double scale_y = 0.9 * PAINT_HEIGHT / (y_max - y_min);
    scale_factor = qMin(scale_x, scale_y);

    // draw points
    painter.setPen(Qt::red);
    painter.setBrush(Qt::red);
    rectCenter = Rectangle(points[0], points[1], points[2], points[3]).getRectCenter();

    painter.drawEllipse(coord(rectCenter), 5, 5);
    painter.drawEllipse(coord(incenterMax), 5, 5);



    // draw triangle
    painter.setPen(QPen(Qt::green, 3));
    painter.setBrush(QBrush(Qt::Dense1Pattern));

    Triangle triangle(points[i_max], points[j_max], points[k_max]);

    painter.drawLine(coord(points[i_max]), coord(points[j_max]));
    painter.drawLine(coord(points[j_max]), coord(points[k_max]));
    painter.drawLine(coord(points[i_max]), coord(points[k_max]));
    painter.setPen(QPen(Qt::blue, 3));
    painter.setBrush(QBrush(Qt::Dense1Pattern));
    painter.drawLine(coord(points[0]), coord(points[1]));
    painter.drawLine(coord(points[1]), coord(points[2]));
    painter.drawLine(coord(points[2]), coord(points[3]));
    painter.drawLine(coord(points[3]), coord(points[0]));

    painter.setPen(QPen(Qt::gray, 3));
    painter.setBrush(QBrush(Qt::Dense1Pattern));
    painter.drawLine(coord(points[0]), coord(points[2]));
    painter.drawLine(coord(points[1]), coord(points[3]));


    painter.setPen(QPen(Qt::black, 3));
    painter.setBrush(QBrush(Qt::Dense1Pattern));
    painter.drawLine(coord(points[i_max]), coord(incenterMax));
    painter.drawLine(coord(points[j_max]), coord(incenterMax));
    painter.drawLine(coord(points[k_max]), coord(incenterMax));
    painter.setPen(QPen(Qt::red, 3));
    painter.drawLine(coord(rectCenter), coord(incenterMax));


    painter.setPen(QPen(Qt::gray, 3));
    painter.setBrush(QBrush(Qt::Dense5Pattern));

    painter.setPen(Qt::red);
    painter.setBrush(Qt::red);

    char txt[] = " 1 {1.11, 1.11}";
    sprintf(txt, "%d {%.2f, %.2f}", 0, incenterMax.x, incenterMax.y);
    painter.drawText(coord(incenterMax), txt);

    sprintf(txt, "%d {%.2f, %.2f}", 0, rectCenter.x, rectCenter.y);
    painter.drawText(coord(rectCenter), txt);

    painter.drawEllipse(coord(points[i_max]), 5, 5);
    sprintf(txt, "%d {%.2f, %.2f}", 0, points[i_max].x, points[i_max].y);
    painter.drawText(coord(points[i_max]), txt);

    painter.drawEllipse(coord(points[j_max]), 5, 5);
    sprintf(txt, "%d {%.2f, %.2f}", 0, points[j_max].x, points[j_max].y);
    painter.drawText(coord(points[j_max]), txt);

    painter.drawEllipse(coord(points[k_max]), 5, 5);
    sprintf(txt, "%d {%.2f, %.2f}", 0, points[k_max].x, points[k_max].y);
    painter.drawText(coord(points[k_max]), txt);

    painter.setPen(QPen(Qt::gray, 3));
    painter.setBrush(QBrush(Qt::Dense5Pattern));
    const double x0 = x_coord(rectCenter.x);
    const double y0 = y_coord(rectCenter.y);
    if (0 <= x0 && x0 <= PAINT_WIDTH && 0 <= y0 && y0 <= PAINT_HEIGHT)
    {
        double startAngle, spanAngle;
        if (incenterMax.x >= 0 && incenterMax.y >= 0
         || incenterMax.x <= 0 && incenterMax.y <= 0) {
            spanAngle = degrees(angle_min) * 16;
            startAngle = 0;
        }
        else {
            startAngle = 90 * 16;
            spanAngle = degrees(angle_min) * 16;
        }

        painter.drawPie(x0-25, y0 - 25, 50, 50, startAngle, spanAngle);
    }
}



