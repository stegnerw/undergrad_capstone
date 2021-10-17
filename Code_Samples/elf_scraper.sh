#!/bin/sh

BEN_DIR=$(realpath $(dirname "$0"))/benign_files
mkdir -p $BEN_DIR
for dir in /bin /usr/bin; do
  find $dir -type f -exec file {}\
  | grep ": ELF" | grep -v $BEN_DIR\
  | cut -d: -f1 | xargs cp -p -t $BEN_DIR/
done
find $BEN_DIR -type f -exec mv '{}' '{}'.benign \;

