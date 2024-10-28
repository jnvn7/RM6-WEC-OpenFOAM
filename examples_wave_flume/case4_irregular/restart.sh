#!/bin/bash
#-----------------------------------------------------------------------------#
# Save the log.solver file after each restart
#-----------------------------------------------------------------------------#
fileName=log.interFoam
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


