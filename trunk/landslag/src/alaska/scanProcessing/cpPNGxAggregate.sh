#!/bin/bash

if [ ! -d "png" ]; then
	mkdir "png"
fi
if [ ! -d "pngX1200" ]; then
	mkdir "pngX1200"
fi
if [ ! -d "pngX160" ]; then
        mkdir "pngX160"
fi
if [ ! -d "png50percent" ]; then
        mkdir "png50percent"
fi

for file in `find . -type f -name '*.png'`; do
	FILENAME=`basename $file | cut -d '.' -f1`
	FILEDIR=$(dirname $file)

	if [[ "$FILEDIR" == *"unnid/pngX1200"* ]] 
	then

		$(cp $FILEDIR/$FILENAME.png pngX1200/$FILENAME.png)

	elif [[ "$FILEDIR" == *"unnid/pngX160"* ]] 
	then

		$(cp $FILEDIR/$FILENAME.png pngX160/$FILENAME.png)

	elif [[ "$FILEDIR" == *"unnid/png50percent"* ]] 
	then

		$(cp $FILEDIR/$FILENAME.png png50percent/$FILENAME.png)

	elif [[ "$FILEDIR" == *"unnid/png"* ]] 
	then

		$(cp $FILEDIR/$FILENAME.png png/$FILENAME.png)

	fi

done

