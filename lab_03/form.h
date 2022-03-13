#ifndef FORM_H
#define FORM_H

#include <QWidget>
#include <QDialog>

namespace Ui {
class Form;
}

class Form : public QWidget
{
    Q_OBJECT

public:
    explicit Form(const QVector<QVector<double>> &ns, int M, QWidget *parent = nullptr);
    ~Form();

private:
    Ui::Form *ui;
};

#endif // FORM_H
