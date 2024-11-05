#!/bin/bash
#-----------------------------------------------------------------------------#
# Script to restart OpenFOAM case
#-----------------------------------------------------------------------------#
fileName=log.overInterDyMFoam
# Move data to backup folder
if [ -f $fileName ]
then
  for i in {1..100}
  do
    dataFolder="data$i"
    if [ ! -d $dataFolder ]
    then
       mkdir $dataFolder
       break
    fi
  done

  # Move data to the storage folder
  mv $fileName $dataFolder/
fi

# Extract latest simulated time (for PARALLEL run only)
if [ -d processor0 ]
then
  time=$(ls -t processor0 | head -n 1)

  # Adjust the restart time
  sed -i "/startTime/s/.*/    startTime\t\t$time;/" flowParams
else
  sed -i "/startTime/s/.*/    startTime\t\t0.0;/" flowParams
fi

