# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.2

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
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
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /storage/fbusato/lib/XLib

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /storage/fbusato/lib/XLib/build

# Include any dependencies generated for this target.
include CMakeFiles/XLib_sm30.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/XLib_sm30.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/XLib_sm30.dir/flags.make

CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_Timer.cu.o: CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_Timer.cu.o.depend
CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_Timer.cu.o: CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_Timer.cu.o.cmake
CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_Timer.cu.o: ../Base/Device/Util/src/Timer.cu
	$(CMAKE_COMMAND) -E cmake_progress_report /storage/fbusato/lib/XLib/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Building NVCC (Device) object CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_Timer.cu.o"
	cd /storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src && /usr/bin/cmake -E make_directory /storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/.
	cd /storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src && /usr/bin/cmake -D verbose:BOOL=$(VERBOSE) -D build_configuration:STRING= -D generated_file:STRING=/storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/./XLib_sm30_generated_Timer.cu.o -D generated_cubin_file:STRING=/storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/./XLib_sm30_generated_Timer.cu.o.cubin.txt -P /storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_Timer.cu.o.cmake

CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_cuda_util.cu.o: CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_cuda_util.cu.o.depend
CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_cuda_util.cu.o: CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_cuda_util.cu.o.cmake
CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_cuda_util.cu.o: ../Base/Device/Util/src/cuda_util.cu
	$(CMAKE_COMMAND) -E cmake_progress_report /storage/fbusato/lib/XLib/build/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Building NVCC (Device) object CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_cuda_util.cu.o"
	cd /storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src && /usr/bin/cmake -E make_directory /storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/.
	cd /storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src && /usr/bin/cmake -D verbose:BOOL=$(VERBOSE) -D build_configuration:STRING= -D generated_file:STRING=/storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/./XLib_sm30_generated_cuda_util.cu.o -D generated_cubin_file:STRING=/storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/./XLib_sm30_generated_cuda_util.cu.o.cubin.txt -P /storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_cuda_util.cu.o.cmake

CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o: CMakeFiles/XLib_sm30.dir/flags.make
CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o: ../Base/Host/src/fUtil.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /storage/fbusato/lib/XLib/build/CMakeFiles $(CMAKE_PROGRESS_3)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o"
	/storage/fbusato/bin/gcc-4.9.2/build/bin/g++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o -c /storage/fbusato/lib/XLib/Base/Host/src/fUtil.cpp

CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.i"
	/storage/fbusato/bin/gcc-4.9.2/build/bin/g++  $(CXX_DEFINES) $(CXX_FLAGS) -E /storage/fbusato/lib/XLib/Base/Host/src/fUtil.cpp > CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.i

CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.s"
	/storage/fbusato/bin/gcc-4.9.2/build/bin/g++  $(CXX_DEFINES) $(CXX_FLAGS) -S /storage/fbusato/lib/XLib/Base/Host/src/fUtil.cpp -o CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.s

CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o.requires:
.PHONY : CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o.requires

CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o.provides: CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o.requires
	$(MAKE) -f CMakeFiles/XLib_sm30.dir/build.make CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o.provides.build
.PHONY : CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o.provides

CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o.provides.build: CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o

CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o: CMakeFiles/XLib_sm30.dir/flags.make
CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o: ../Base/Host/src/Timer.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /storage/fbusato/lib/XLib/build/CMakeFiles $(CMAKE_PROGRESS_4)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o"
	/storage/fbusato/bin/gcc-4.9.2/build/bin/g++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o -c /storage/fbusato/lib/XLib/Base/Host/src/Timer.cpp

CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.i"
	/storage/fbusato/bin/gcc-4.9.2/build/bin/g++  $(CXX_DEFINES) $(CXX_FLAGS) -E /storage/fbusato/lib/XLib/Base/Host/src/Timer.cpp > CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.i

CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.s"
	/storage/fbusato/bin/gcc-4.9.2/build/bin/g++  $(CXX_DEFINES) $(CXX_FLAGS) -S /storage/fbusato/lib/XLib/Base/Host/src/Timer.cpp -o CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.s

CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o.requires:
.PHONY : CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o.requires

CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o.provides: CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o.requires
	$(MAKE) -f CMakeFiles/XLib_sm30.dir/build.make CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o.provides.build
.PHONY : CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o.provides

CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o.provides.build: CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o

# Object files for target XLib_sm30
XLib_sm30_OBJECTS = \
"CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o" \
"CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o"

# External object files for target XLib_sm30
XLib_sm30_EXTERNAL_OBJECTS = \
"/storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_Timer.cu.o" \
"/storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_cuda_util.cu.o"

libXLib_sm30.a: CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o
libXLib_sm30.a: CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o
libXLib_sm30.a: CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_Timer.cu.o
libXLib_sm30.a: CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_cuda_util.cu.o
libXLib_sm30.a: CMakeFiles/XLib_sm30.dir/build.make
libXLib_sm30.a: CMakeFiles/XLib_sm30.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX static library libXLib_sm30.a"
	$(CMAKE_COMMAND) -P CMakeFiles/XLib_sm30.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/XLib_sm30.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/XLib_sm30.dir/build: libXLib_sm30.a
.PHONY : CMakeFiles/XLib_sm30.dir/build

CMakeFiles/XLib_sm30.dir/requires: CMakeFiles/XLib_sm30.dir/Base/Host/src/fUtil.cpp.o.requires
CMakeFiles/XLib_sm30.dir/requires: CMakeFiles/XLib_sm30.dir/Base/Host/src/Timer.cpp.o.requires
.PHONY : CMakeFiles/XLib_sm30.dir/requires

CMakeFiles/XLib_sm30.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/XLib_sm30.dir/cmake_clean.cmake
.PHONY : CMakeFiles/XLib_sm30.dir/clean

CMakeFiles/XLib_sm30.dir/depend: CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_Timer.cu.o
CMakeFiles/XLib_sm30.dir/depend: CMakeFiles/XLib_sm30.dir/Base/Device/Util/src/XLib_sm30_generated_cuda_util.cu.o
	cd /storage/fbusato/lib/XLib/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /storage/fbusato/lib/XLib /storage/fbusato/lib/XLib /storage/fbusato/lib/XLib/build /storage/fbusato/lib/XLib/build /storage/fbusato/lib/XLib/build/CMakeFiles/XLib_sm30.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/XLib_sm30.dir/depend

