cmake_minimum_required(VERSION 3.1)

project(duo_lvgl_py)

include_directories(.)
add_subdirectory(lvgl)
add_subdirectory(lv_drivers)

add_executable(${PROJECT_NAME} main.c mouse_cursor_icon.c)
target_link_libraries(${PROJECT_NAME} PRIVATE lvgl lvgl::drivers)
