#include "mainwindow.h"
#include "ui_mainwindow.h"


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    scene = new QGraphicsScene(0, 0, PAINT_WIDTH, PAINT_HEIGHT);
    ui->graphicsView->setScene(scene);

    initPoints();
    drawOriginalImage();
}

MainWindow::~MainWindow()
{
    delete ui;
}



double MainWindow::x_coord(double x) const
{
    return PAINT_WIDTH / 2 + x * NORMAL_SCALE_FACTOR / compress;
}

double MainWindow::y_coord(double y) const
{
    return PAINT_HEIGHT / 2 - y * NORMAL_SCALE_FACTOR / compress;
}

QPointF MainWindow::coord(const Point &point) const
{
    return QPointF(x_coord(point.x), y_coord(point.y));
}

double MainWindow::anti_coord_x(double x) const
{
    return (-PAINT_WIDTH / 2 + x) / NORMAL_SCALE_FACTOR * compress;
}

double MainWindow::anti_coord_y(double y) const
{
    return (PAINT_HEIGHT / 2 - y) / NORMAL_SCALE_FACTOR * compress;
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



void MainWindow::drawOriginalImage()
{
    scene->clear();
    Transform transform;
    for (int i = transforms.size() - 1; i >= 0; --i)
        transform.combine(transforms[i]);

    compress = 1;

    const Point paint_size(
        PAINT_WIDTH / (2.0 * NORMAL_SCALE_FACTOR),
        PAINT_HEIGHT / (2.0 * NORMAL_SCALE_FACTOR)
    );

    const Point paint_min(4, 1.5);

    Point paint_max;

    QVector<Point> _rhomb(4);
    for (int i = 0; i != 4; ++i)
    {
        _rhomb[i] = transform.apply(points[i]);
        paint_max.x = qMax(qAbs(_rhomb[i].x), paint_max.x);
        paint_max.y = qMax(qAbs(_rhomb[i].y), paint_max.y);
    }
    for (int i = 0; i < points.length(); i++)
    {
        paint_max.x = qMax(qAbs(points[i].x), paint_max.x);
        paint_max.y = qMax(qAbs(points[i].y), paint_max.y);
    }

    if (autoscaling)
    {
        if (paint_max.x > paint_size.x || paint_max.y > paint_size.y)
            compress *= 1.1 * qMax(paint_max.x / paint_size.x, paint_max.y / paint_size.y);
        else if (paint_max.x < paint_min.x && paint_max.y < paint_min.y)
        {
            compress *= 1.1 * qMax(paint_max.x / paint_size.x, paint_max.y / paint_size.y);
            if (compress == 0)
                compress = 1e-12;
        }
    }

    QVector<QPointF> rhomb(4);
    QVector<QPointF> circle(n);
    for (int i = 0; i != 4; ++i)
        rhomb[i] = coord(_rhomb[i]);
    QVector<QPointF> astroida(n);
    for (int i = 0; i != n; ++i)
        astroida[i] = coord(transform.apply(points[i + 4]));
    for (int i = 0; i < n; ++i)
        circle[i] = coord(transform.apply(points[n + 4 + i]));
    QVector<QPointF> central_point(2);
    central_point[0] = coord(transform.apply(points[2 * n + 1]));
    central_point[1] = coord(transform.apply(points[2 * n + 2]));
    //int m = PAINT_HEIGHT * compress / (2 * NORMAL_SCALE_FACTOR);
    for (int i = 0; i < 3; ++i)
        scene->addLine(QLineF(rhomb[i], rhomb[i + 1]));
    for (int i = 0; i < n - 1; ++i)
    {
        QPolygonF polygon;
        polygon << astroida[i] << astroida[i + 1];
        scene->addPolygon(polygon);
    }
    for (int i = 0; i < n - 5; ++i)
    {
        QPolygonF polygon;
        polygon << circle[i] << circle[i + 1];
        scene->addPolygon(polygon);
    }
    scene->addEllipse(QRectF(central_point[0].x() - 1, central_point[0].y() - 1,
            2, 2), QPen(Qt::red));
    char txt[] = " {1.11, 1.11}";
    QGraphicsTextItem *num = new QGraphicsTextItem;
    num->setPos(central_point[0]);
    sprintf(txt, "{%.2f, %.2f}", anti_coord_x(central_point[0].x()), anti_coord_y(central_point[0].y()));
    num->setPlainText(QString(txt));

    scene->addItem(num);
}

void MainWindow::initPoints()
{
    points = QVector<Point>(2 * n + 6);

    points[0] = Point(-3, 0);
    points[1] = Point(-3, -5);
    points[2] = Point(3, -5);
    points[3] = Point(3, 0);

    for (int i = 0; i < n; ++i)
    {
        double t = 2 * M_PI * i / n;
        double cost = std::cos(t);
        double sint = std::sin(t);
        points[i + 4] = Point(
            b * cost * cost * cost,
            a * sint * sint * sint
        );
    }
    for (int i = n + 4; i < 2 * n; ++i)
    {
        double t = 2 * M_PI * (i - n + 4) / n;
        double cost = std::cos(t);
        double sint = std::sin(t);
        points[i] = Point(
            cost,
            sint
        );
    }
    points[2 * n + 1] = Point(0, 0);
    points[2 * n + 2] = Point(0.0001, 0.0001);

}

bool MainWindow::get_var(double &var, const QLineEdit *lineEdit, const QString &err_msg)
{
    bool ok;
    var = lineEdit->text().toDouble(&ok);
    if (!ok)
        ui->statusbar->showMessage(err_msg, STATUS_BAR_TIMEOUT);
    return ok;
}


void MainWindow::on_pushButtonTransfer_clicked()
{
    if (!(get_var(x, ui->xCoordLine, "Неверно введена координата x перемещения")
           && get_var(y, ui->yCoordEdit, "Неверно введена координата y перемещения")))
            return;
    Transform translation;
    translation.translate(Point(x, y));
    transforms.push_back(translation);

    drawOriginalImage();

    ui->statusbar->showMessage("Перемещение прошло успешно", STATUS_BAR_TIMEOUT);
    update();
}


void MainWindow::on_pushButtonScale_clicked()
{
    double x, y, kx, ky;
    if (!(get_var(x, ui->xCoordLine, "Неверно введена координата x перемещения")
       && get_var(y, ui->yCoordEdit, "Неверно введена координата y перемещения")
       && get_var(kx, ui->xCoefEdit, "Неверно введена координата kx масташтабирования")
       && get_var(ky, ui->yCoefEdit, "Неверно введена координата ky масташтабирования")))
        return;

    Transform scaling;
    scaling.scale(Point(kx, ky), Point(x, y));
    transforms.push_back(scaling);

    drawOriginalImage();

    ui->statusbar->showMessage("Масташтабирование прошло успешно", STATUS_BAR_TIMEOUT);
    update();
}


void MainWindow::on_pushButtonTurn_clicked()
{
    double x, y, alpha;
    if (!(get_var(x, ui->xCoordLine, "Неверно введена координата x перемещения")
       && get_var(y, ui->yCoordEdit, "Неверно введена координата y перемещения")
       && get_var(alpha, ui->angleEdit, "Неверно введен угол поворота")))
        return;

    Transform rotation;
    rotation.rotate(alpha * M_PI / 180, Point(x, y));
    transforms.push_back(rotation);

    drawOriginalImage();

    ui->statusbar->showMessage("Поворот проведен успешно", STATUS_BAR_TIMEOUT);
    update();
}


void MainWindow::on_pushButtonBack_clicked()
{
    if (transforms.empty())
    {
        ui->statusbar->showMessage("Нельзя вернуться назад");
        return;
    }

    transforms.pop_back();

    drawOriginalImage();

    ui->statusbar->showMessage("Успешно возращено назад", STATUS_BAR_TIMEOUT);
    update();
}


void MainWindow::on_checkBox_stateChanged(int arg1)
{
    autoscaling = arg1;
    on_pushButtonOriginal_clicked();
}


void MainWindow::on_pushButtonOriginal_clicked()
{
    while (!transforms.isEmpty())
        transforms.pop_back();
    drawOriginalImage();
    ui->statusbar->showMessage("Успешно возращено назад", STATUS_BAR_TIMEOUT);
    update();
}

