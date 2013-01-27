#!/bin/bash

CONVERT_CMD=/home/bthj/ImageMagick/bin/convert

for file in `find . -type f -name '*.tif'`; do
	FILENAME=`basename $file | cut -d '.' -f1`
	FILEDIR=$(dirname $file)

	if [[ "$FILEDIR" == *"unnid"* ]] 
	then



		echo file: $file - filename: $FILENAME - fieldir: $FILEDIR
		if [ ! -d "$FILEDIR/png" ]; then
			mkdir "$FILEDIR/png"
		fi
		if [ ! -d "$FILEDIR/pngX1200" ]; then
		        mkdir "$FILEDIR/pngX1200"
		fi
		if [ ! -d "$FILEDIR/pngX160" ]; then
		        mkdir "$FILEDIR/pngX160"
		fi
	#        if [ ! -d "$FILEDIR/png300dpi" ]; then
	#                mkdir "$FILEDIR/png300dpi"
	#        fi
		if [ ! -d "$FILEDIR/png50percent" ]; then
		        mkdir "$FILEDIR/png50percent"
		fi
		if [ ! -d "$FILEDIR/MPC" ]; then
		        mkdir "$FILEDIR/MPC"
		fi


		# let's create a "memory-mapped disk file of program memory, saved to disk as two binary files"
		if [ ! -f "$FILEDIR/png/$FILENAME.png" -o ! -f "$FILEDIR/pngX1200/$FILENAME.png" -o ! -f "$FILEDIR/pngX160/$FILENAME.png" -o ! -f "$FILEDIR/png50percent/$FILENAME.png" ]; then
			echo vinn $FILEDIR/MPC/$FILENAME.mpc
			$($CONVERT_CMD $file $FILEDIR/MPC/$FILENAME.mpc)
		fi

		if [ ! -f "$FILEDIR/png/$FILENAME.png" ]; then
			echo vinn $FILEDIR/png/$FILENAME.png
			$($CONVERT_CMD $FILEDIR/MPC/$FILENAME.mpc $FILEDIR/png/$FILENAME.png)
		fi

		if [ ! -f "$FILEDIR/pngX1200/$FILENAME.png" ]; then
			echo vinn $FILEDIR/pngX1200/$FILENAME.png
			$($CONVERT_CMD -resize x1200\> $FILEDIR/MPC/$FILENAME.mpc $FILEDIR/pngX1200/$FILENAME.png)
		fi

		if [ ! -f "$FILEDIR/pngX160/$FILENAME.png" ]; then
			echo vinn $FILEDIR/pngX160/$FILENAME.png
			$($CONVERT_CMD -resize x160\> $FILEDIR/MPC/$FILENAME.mpc $FILEDIR/pngX160/$FILENAME.png)
		fi

	#	if [ ! -f "$FILEDIR/png300dpi/$FILENAME.png" ]; then
	#		echo vinn $FILEDIR/png300dpi/$FILENAME.png
	#		$($CONVERT_CMD -units PixelsPerInch $file -resample 300 $FILEDIR/png300dpi/$FILENAME.png)
	#	fi

		if [ ! -f "$FILEDIR/png50percent/$FILENAME.png" ]; then
			echo vinn $FILEDIR/png50percent/$FILENAME.png
			$($CONVERT_CMD $FILEDIR/MPC/$FILENAME.mpc -resize 50% $FILEDIR/png50percent/$FILENAME.png)
		fi

		rm -f "$FILEDIR/MPC/$FILENAME.mpc" "$FILEDIR/MPC/$FILENAME.cache"



	fi


done
