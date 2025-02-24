#include "polygon_area_calculator.h"

void polygon_area_calculator::print_polygons( std::vector<Polygon>& polygons ) {
    for (auto& polygon : polygons) {
        std::cout << polygon << std::endl;
    }
}