#include "logic.h"
#include <cmath>
#include <cassert>

double degrees(double radians)
{
    return radians * 180 / M_PI;
}

Point::Point(double x, double y): x(x), y(y){ }

Point::Point(const Point& A, const Point& B)
    : x(B.x - A.x)
    , y(B.y - A.y)
    { }

Point Point::perpendicular() const
{
    return Point(y, -x);
}

Point Point::unit() const
{
    double norm = Point::norm();
    return Point(x / norm, y / norm);
}

double Point::norm() const
{
    return sqrt(x * x + y * y);
}

double Point::angle() const
{
    return std::atan2(y, x);
}

double dot_product(const Point& A, const Point& B)
{
    return A.x * B.x + A.y * B.y;
}

double skew_product(const Point& A, const Point& B)
{
    return A.x * B.y - A.y * B.x;
}

double angle(const Point& A, const Point& B) {
    return B.angle() - A.angle();
}

bool on_one_line(const Point& A, const Point& B, const Point& C)
{
    return std::abs(skew_product(Point(A, B), Point(A, C))) < EPS;
}

double& Point::operator[](int i)
{
    assert(i == 0 || i == 1);
    return i ? y : x;
}


Point operator-(const Point& A, const Point& B) {
    return Point(B, A);
}

bool operator==(const Point& A, const Point& B) {
    return std::abs(A.x - B.x) < EPS && std::abs(A.y - B.y) < EPS;
}

bool operator!=(const Point& A, const Point& B) {
    return !(A == B);
}

std::istream& operator>>(std::istream& is, Point& point) {
    is >> point.x >> point.y;
    return is;
}

std::ostream& operator<<(std::ostream& os, const Point& point) {
    os << '(' << point.x << ", " << point.y << ')';
    return os;
}


Line::Line(double A, double B, double C)
    : A(A)
    , B(B)
    , C(C)
    { }

Line::Line(const Point& A, const Point& B)
    : A(A.y - B.y)
    , B(B.x - A.x)
    , C(skew_product(A, B)) {}


Point Line::normal_vector() const
{
    return Point(A, B);
}

Point Line::directing_vector() const
{
    return normal_vector().perpendicular();
}

Line Line::perpendicular(const Point& point) const
{
    Point dv = directing_vector();
    return Line(dv.x, dv.y, -(dv.x * point.x + dv.y * point.y));
}

Point intersection(const Line& a, const Line& b)
{
    double delta = a.A * b.B - a.B * b.A;
    assert(std::abs(delta) > EPS);
    double delta_x = -a.C * b.B + a.B * b.C;
    double delta_y = -a.A * b.C + a.C * b.A;
    return Point(delta_x / delta, delta_y / delta);
}

double angle(const Line& a, const Line& b)
{
    if (parallel(a, b))
        return 0.0;
    Point a_nv = a.normal_vector();
    Point b_nv = b.normal_vector();
    double phi = std::acos(std::abs(dot_product(a_nv, b_nv)) / (a_nv.norm() * b_nv.norm()));
    return phi < M_PI / 2 ? phi : M_PI - phi;
}

bool parallel(const Line& a, const Line& b)
{
    return std::abs(a.A * b.B - a.B * b.A) < EPS;
}

std::ostream& operator<<(std::ostream& os, const Line& line)
{
    os << line.A << "x + " << line.B << "y + " << line.C << " = 0";
    return os;
}

Triangle::Triangle(const Point& A, const Point& B, const Point& C)
{

    Triangle::A = A;
    Triangle::B = B;
    Triangle::C = C;
}

double getLength(Point A, Point B)
{
    double len = sqrt((B.x - A.x) * (B.x - A.x) + (B.y - A.y) * (B.y - A.y));
    return len;
}

Point Triangle::incenter() const
{
    double x, y;
    x = ((getLength(A, B) * C.x + getLength(A, C) * B.x + getLength(C, B) * A.x) /
         (getLength(A, B) + getLength(A, C) + getLength(B, C)));
    y = ((getLength(A, B) * C.y + getLength(A, C) * B.y + getLength(C, B) * A.y) /
         (getLength(A, B) + getLength(A, C) + getLength(B, C)));
    return Point(x, y);
}

bool Triangle::includes(const Point &point) const
{
    double sgn_a = skew_product(Point(B, C), point);
    double sgn_b = skew_product(Point(C, A), point);
    double sgn_c = skew_product(Point(A, B), point);

    return (sgn_a >= 0 && sgn_b >= 0 && sgn_c >= 0) || (sgn_a <= 0 && sgn_b <= 0 && sgn_c <= 0);
}

std::ostream& operator<<(std::ostream& os, const Triangle& triangle)
{
    os << triangle.A << ", " << triangle.B << ", " << triangle.C;
    return os;
}

Point Rectangle::getRectCenter() const
{
    Line AC = Line(A, C);
    Line BD = Line(B, D);
    return intersection(AC, BD);
}

std::ostream& operator<<(std::ostream& os, const Rectangle& rect)
{
    os << rect.A << ", " << rect.B << ", " << rect.C << ", " << rect.D;
    return os;
}

Rectangle::Rectangle(const Point& A, const Point& B, const Point& C, const Point& D)
{

    Rectangle::A = A;
    Rectangle::B = B;
    Rectangle::C = C;
    Rectangle::D = D;
}

Line getCenterLine(Rectangle Rect, Triangle Tri)
{
    Point A = Rect.getRectCenter();
    Point B = Tri.incenter();
    return Line(A, B);
}

double getAngle(Line A)
{
    Line abscissa = Line(Point(0, 0), Point(1, 0));
    return angle(A, abscissa);
}

bool isRect(Point A, Point B, Point C, Point D)
{
    Line AB = Line(A, B);
    Line AD = Line(A, D);
    Line CD = Line(C, D);
    Line BC = Line(B, C);

    if ((getLength(A, B) > EPS) && (getLength(B, C) > EPS) && (getLength(C, D) > 0) && (getLength(D, A) > 0))
        if (parallel(AB, CD) && parallel(AD, BC) && angle(AB, AD) - 90 < EPS  && angle(CD, AD) - 90 < EPS  && angle(CD, BC) - 90 < EPS)
            return true;
    return false;
}
