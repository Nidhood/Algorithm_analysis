cmake_minimum_required(VERSION 3.24)
project(Polygon_Area_Calculator CXX)

set(CMAKE_CXX_STANDARD 17)
add_executable(area
        main.cxx
        src/polygon_area_calculator.cxx
)

include_directories(include)
include_directories(src)