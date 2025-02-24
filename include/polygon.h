#ifndef POLYGON_H
#define POLYGON_H

#include <iostream>


class Polygon {

  private:
    float upper_left_x;
    float upper_left_y;
    float lower_right_x;
    float lower_right_y;
    float area;

  public:
    Polygon(const float upper_left_x, const float upper_left_y, const float lower_right_x, const float lower_right_y) : upper_left_x(upper_left_x), upper_left_y(upper_left_y), lower_right_x(lower_right_x), lower_right_y(lower_right_y) {
        area = (lower_right_x - upper_left_x) * (upper_left_y - lower_right_y);
    }
    float get_upper_left_x() const { return upper_left_x; }
    float get_upper_left_y() const { return upper_left_y; }
    float get_lower_right_x() const { return lower_right_x; }
    float get_lower_right_y() const { return lower_right_y; }
    float get_area() const { return area; }
    friend std::ostream& operator<<(std::ostream& os, const Polygon& polygon) {
        os << "[" << polygon.upper_left_x << ", " << polygon.upper_left_y << ", " << polygon.lower_right_x << ", " << polygon.lower_right_y << "]";
    }
    bool operator==(const Polygon& rhs) const {
        return upper_left_x == rhs.upper_left_x && upper_left_y == rhs.upper_left_y && lower_right_x == rhs.lower_right_x && lower_right_y == rhs.lower_right_y && position == rhs.position && area == rhs.area;
    }
};

#endif //POLYGON_H
