#!/bin/bash

# Braccio Robotioco Matera
# Build script per i componenti su Raspberry

# Casa Corsini - Alberto Trentadue 2019

VERSION_STRING="dev-190406"
PACKAGE_BASE_NAME="Fanny-RPi"

# Take the start location
SOURCE_DIR=`pwd`

#Check build dir location
if [ -z $ZMOIST_COLL_BUILDDIR ]; then
  FANNY_RPI_BUILDDIR="../../../BUILD/FANNY_RPI"
fi
mkdir -p $FANNY_RPI_BUILDDIR
if [ $? -ne 0 ]; then
  echo "Impossibile creare la directory di build. Uscita."
  exit 1
fi

cd $FANNY_RPI_BUILDDIR
BASE_DIR="fanny"
mkdir -p $BASE_DIR
# Cleanup the existing, if any
cd $BASE_DIR
rm -rf Downloader
rm -rf movemaker

# Make the Drawings dirs
mkdir -p Drawings
cd Drawings
mkdir -p downloads
mkdir -p staged
mkdir -p archived
cd ..

# Copy Downloader's scripts
mkdir Downloader
cd Downloader
cp $SOURCE_DIR/Downloader/*.py .
cd ..

# Copy movemaker's scripts
mkdir movemaker
cd movemaker
cp $SOURCE_DIR/movemaker/*.py .
cd ..

# Make the compressed package
cd ..
PACKAGE_NAME=$PACKAGE_BASE_NAME"-"$VERSION_STRING
rm -f $PACKAGE_NAME".tgz"
tar czf $PACKAGE_NAME".tgz" $BASE_DIR

cd $SOURCE_DIR
echo "Collector package $PACKAGE_NAME created."

