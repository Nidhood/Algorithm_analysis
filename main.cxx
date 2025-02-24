#include <iostream>

#include "polygon_area_calculator.h"

int main()
{
    // Create polygons:
    const Polygon polygon1(0.0, 6.0, 3.0, 3.0);
    const Polygon polygon2(1.0, 3.0, 4.0, 2.0);
    const Polygon polygon3(2.0, 4.0, 5.0, 3.0);
    const Polygon polygon4(4.0, 6.0, 6.0, 1.0);

    // Create vector of polygons:
    std::vector<Polygon> polygons = {polygon1, polygon2, polygon3, polygon4};
    polygon_area_calculator::print_polygons(polygons);
    return 0;
}