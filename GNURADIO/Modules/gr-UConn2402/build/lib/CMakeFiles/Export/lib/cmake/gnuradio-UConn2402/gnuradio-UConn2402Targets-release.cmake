#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-UConn2402" for configuration "Release"
set_property(TARGET gnuradio::gnuradio-UConn2402 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(gnuradio::gnuradio-UConn2402 PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libgnuradio-UConn2402.so.1.0.0.0"
  IMPORTED_SONAME_RELEASE "libgnuradio-UConn2402.so.1.0.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-UConn2402 )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-UConn2402 "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libgnuradio-UConn2402.so.1.0.0.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
