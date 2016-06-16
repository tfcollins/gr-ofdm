INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_OFDM ofdm)

FIND_PATH(
    OFDM_INCLUDE_DIRS
    NAMES ofdm/api.h
    HINTS $ENV{OFDM_DIR}/include
        ${PC_OFDM_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    OFDM_LIBRARIES
    NAMES gnuradio-ofdm
    HINTS $ENV{OFDM_DIR}/lib
        ${PC_OFDM_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(OFDM DEFAULT_MSG OFDM_LIBRARIES OFDM_INCLUDE_DIRS)
MARK_AS_ADVANCED(OFDM_LIBRARIES OFDM_INCLUDE_DIRS)

