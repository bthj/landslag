#!/bin/bash

#QMAX=42
QMAX=51

#BITRATE="-vb 2M"
BITRATE="-b 1500k"

AUDIO_QUALITY="-aq 90"
#AUDIO_QUALITY="-ab 128k"

#FRAME_SIZE=""
#FRAME_SIZE="-s 720x576"
FRAME_SIZE="-s 768x576"

ffmpeg -y -i $1 -threads 0 $FRAME_SIZE -vcodec libx264 -vpre slow_firstpass -vpre baseline -deinterlace -g 120 -qmax $QMAX -qmin 10 -rc_buf_aggressivity 0.95 $BITRATE -pass 1  $1.mp4
ffmpeg -y -i $1 -threads 0 $FRAME_SIZE -vcodec libx264 -vpre slow -vpre baseline -deinterlace -g 120  -qmax $QMAX -qmin 10 -rc_buf_aggressivity 0.95 $BITRATE -pass 2 -acodec libfaac $AUDIO_QUALITY -ac 2  $1.mp4

ffmpeg -y -i $1 -threads 4 $FRAME_SIZE -f webm -vcodec libvpx -deinterlace -g 120 -level 216 -profile 0 -qmax $QMAX -qmin 10 -rc_buf_aggressivity 0.95 $BITRATE -pass 1  $1.webm
ffmpeg -y -i $1 -threads 4 $FRAME_SIZE -f webm -vcodec libvpx -deinterlace -g 120 -level 216 -profile 0 -qmax $QMAX -qmin 10 -rc_buf_aggressivity 0.95 $BITRATE -pass 2 -acodec libvorbis $AUDIO_QUALITY -ac 2  $1.webm

ffmpeg -y -i $1 -threads 4 $FRAME_SIZE -vcodec libtheora -deinterlace -g 120 -level 216 -profile 0 -qmax $QMAX -qmin 10 -rc_buf_aggressivity 0.95 $BITRATE -pass 1  $1.ogv
ffmpeg -y -i $1 -threads 4 $FRAME_SIZE -vcodec libtheora -deinterlace -g 120 -level 216 -profile 0 -qmax $QMAX -qmin 10 -rc_buf_aggressivity 0.95 $BITRATE -pass 2 -acodec libvorbis $AUDIO_QUALITY -ac 2 $1.ogv

