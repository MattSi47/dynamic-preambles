# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT UConn2402_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT UConn2402_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################
list(APPEND UConn2402_python_files
    LFMChirpXCorr_python.cc
    Chirp_python.cc
    ArbitrarySync_python.cc
    ArbitrarySync2_python.cc
    Preamble_python.cc
    fftXCorr_python.cc python_bindings.cc)

GR_PYBIND_MAKE_OOT(UConn2402
   ../../..
   gr::UConn2402
   "${UConn2402_python_files}")

# copy in bindings .so file for use in QA test module
add_custom_target(
  copy_bindings_for_tests ALL
  COMMAND
    ${CMAKE_COMMAND} -E copy "${CMAKE_CURRENT_BINARY_DIR}/*.so"
    ${CMAKE_BINARY_DIR}/test_modules/gnuradio/UConn2402/
  DEPENDS UConn2402_python)

install(TARGETS UConn2402_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/UConn2402 COMPONENT pythonapi)
