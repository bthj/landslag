#!/bin/bash

PNG_DIR="./png"
PNG_X1200_DIR="./pngx1200"
PNG_X160_DIR="./pngx160"

#if [[ ! -d "$PNG_DIR" && ! -L "$PNG_DIR" ]] ; then
#  mkdir --parents "$PNG_DIR"
#fi

#for file in `find . -type f -name '*.tif'`; do
#  FILE_NAME_BASE=`basename "$file" .tif`
#  echo "converting $file to PNG: $FILE_NAME_BASE.png"
#  $(convert $file $PNG_DIR/$FILE_NAME_BASE.png) 2>errorPngConvert.log
#done

for file in `find . -type f -name '*.tif'`; do
  FILE_NAME_BASE=`basename "$file" .tif`
  echo "converting $file to PNG: $FILE_NAME_BASE.png"
  $(convert -resize 'x1200' $file $PNG_X1200_DIR/$FILE_NAME_BASE.png) 2>errorPngConvert.log
done

for file in `find . -type f -name '*.tif'`; do
  FILE_NAME_BASE=`basename "$file" .tif`
  echo "converting $file to PNG: $FILE_NAME_BASE.png"
  $(convert -resize 'x160' $file $PNG_X160_DIR/$FILE_NAME_BASE.png) 2>errorPngConvert.log
done
