#ifndef POLYGON_AREA_CALCULATOR_H
#define POLYGON_AREA_CALCULATOR_H

#include <vector>
#include <string>
#include "polygon.h"

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// Inputs: 2D points in the form of a vector of pairs
// Outputs: Union of the area of the polygons inside the vector of tuples.
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


namespace polygon_area_calculator {
    void print_polygons(std::vector<Polygon>& polygons);
    double calculate_area(const std::vector<Polygon *>& polygons);
}

#endif //POLYGON_AREA_CALCULATOR_H
