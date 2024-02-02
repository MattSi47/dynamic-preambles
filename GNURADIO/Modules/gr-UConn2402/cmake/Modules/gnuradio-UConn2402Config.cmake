find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_UCONN2402 gnuradio-UConn2402)

FIND_PATH(
    GR_UCONN2402_INCLUDE_DIRS
    NAMES gnuradio/UConn2402/api.h
    HINTS $ENV{UCONN2402_DIR}/include
        ${PC_UCONN2402_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_UCONN2402_LIBRARIES
    NAMES gnuradio-UConn2402
    HINTS $ENV{UCONN2402_DIR}/lib
        ${PC_UCONN2402_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-UConn2402Target.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_UCONN2402 DEFAULT_MSG GR_UCONN2402_LIBRARIES GR_UCONN2402_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_UCONN2402_LIBRARIES GR_UCONN2402_INCLUDE_DIRS)
