#ifndef LOGIC_H
#define LOGIC_H

#include <istream>
#include <ostream>

#define EPS 1E-5

double degrees(double radians);


struct Point
{
    double x, y;
    Point(double x = 0, double y = 0);
    Point(const Point& A, const Point& B);
    Point perpendicular() const;
    Point unit() const;
    double norm() const;
    double angle() const;

    double& operator[](int i);
};

double dot_product(const Point& A, const Point& B);
double skew_product(const Point& A, const Point& B);

double angle(const Point& A, const Point& B);

bool on_one_line(const Point& A, const Point& B, const Point& C);

Point operator-(const Point& A, const Point& B);
bool operator==(const Point& A, const Point& B);
bool operator!=(const Point& A, const Point& B);

std::istream& operator>>(std::istream& is, Point& point);
std::ostream& operator<<(std::ostream& os, const Point& point);



struct Line
{
    double A, B, C;

    Line(double A, double B, double C);
    Line(const Point& A, const Point& B);

    Point normal_vector() const;
    Point directing_vector() const;
    Line perpendicular(const Point& point) const;


};

Point intersection(const Line& a, const Line& b);

double angle(const Line& a, const Line& b);

double getLength(Point A, Point B);

bool parallel(const Line& a, const Line& b);

std::ostream& operator<<(std::ostream& os, const Line& line);


struct Triangle
{
    Point A, B, C;

    Triangle(const Point& A, const Point& B, const Point& C);

    // Line altitude();
    Point incenter() const;
    bool includes(const Point& point) const;
};

std::ostream& operator<<(std::ostream& os, const Triangle& triangle);

struct Rectangle
{
    Point A, B, C, D;

    Rectangle(const Point& A, const Point&B, const Point& C, const Point& D);

    Point getRectCenter() const;

};

std::ostream& operator<<(std::ostream& os, const Rectangle& rect);

Line getCenterLine(Rectangle Rect, Triangle Tri);

double getAngle(Line A);

bool isRect(Point A, Point B, Point C, Point D);

#endif // LOGIC_H
