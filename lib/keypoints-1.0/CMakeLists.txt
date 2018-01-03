cmake_minimum_required(VERSION 2.8)
project( keypoints )
find_package( OpenCV REQUIRED )

add_library( vl_common vl_common.cpp)
add_library( vl_keypoints vl_keypoints.cpp)
add_library( vl_linesedges vl_linesedges.cpp)

add_executable( testkps testkps.cpp )
add_executable( testvideo testvideo.cpp )

target_link_libraries( testkps vl_keypoints vl_common ${OpenCV_LIBS})
target_link_libraries( testvideo vl_keypoints vl_common ${OpenCV_LIBS})

# Generate documentation
find_package(Doxygen)
if(DOXYGEN_FOUND)
    configure_file(Doxyfile.in ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile @ONLY)
        add_custom_target(doc
                ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
                WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
                COMMENT "Generating API documentation with Doxygen" VERBATIM
                )
endif(DOXYGEN_FOUND)

