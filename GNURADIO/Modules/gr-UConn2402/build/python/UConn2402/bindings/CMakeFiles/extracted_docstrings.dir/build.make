# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402/build

# Utility rule file for extracted_docstrings.

# Include any custom commands dependencies for this target.
include python/UConn2402/bindings/CMakeFiles/extracted_docstrings.dir/compiler_depend.make

# Include the progress variables for this target.
include python/UConn2402/bindings/CMakeFiles/extracted_docstrings.dir/progress.make

python/UConn2402/bindings/CMakeFiles/extracted_docstrings: python/UConn2402/bindings/extracted_docstrings.json

python/UConn2402/bindings/extracted_docstrings.json: lib/libgnuradio-UConn2402.so.1.0.0.0
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Scraping generated documentation for docstrings ..."
	cd /home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402/build/python/UConn2402/bindings && /usr/bin/python3 /home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402/docs/doxygen/update_pydoc.py scrape --xml_path /home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402/build/docs/doxygen/xml --json_path /home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402/build/python/UConn2402/bindings/extracted_docstrings.json

extracted_docstrings: python/UConn2402/bindings/CMakeFiles/extracted_docstrings
extracted_docstrings: python/UConn2402/bindings/extracted_docstrings.json
extracted_docstrings: python/UConn2402/bindings/CMakeFiles/extracted_docstrings.dir/build.make
.PHONY : extracted_docstrings

# Rule to build all files generated by this target.
python/UConn2402/bindings/CMakeFiles/extracted_docstrings.dir/build: extracted_docstrings
.PHONY : python/UConn2402/bindings/CMakeFiles/extracted_docstrings.dir/build

python/UConn2402/bindings/CMakeFiles/extracted_docstrings.dir/clean:
	cd /home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402/build/python/UConn2402/bindings && $(CMAKE_COMMAND) -P CMakeFiles/extracted_docstrings.dir/cmake_clean.cmake
.PHONY : python/UConn2402/bindings/CMakeFiles/extracted_docstrings.dir/clean

python/UConn2402/bindings/CMakeFiles/extracted_docstrings.dir/depend:
	cd /home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402 /home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402/python/UConn2402/bindings /home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402/build /home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402/build/python/UConn2402/bindings /home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Modules/gr-UConn2402/build/python/UConn2402/bindings/CMakeFiles/extracted_docstrings.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : python/UConn2402/bindings/CMakeFiles/extracted_docstrings.dir/depend

