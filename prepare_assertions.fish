#!/usr/bin/env fish

set BASEDIR (dirname (status --current-filename))

echo "Activating virtualenv"
source ~/conceptnet5-virtualenv/bin/activate.fish

echo "Changing the directory to conceptnet5 repo"
cd ~/conceptnet5

echo "Building ConceptNet5 assertions.csv, assertions.msgpack"
$BASEDIR/system_requirements.py snakemake --resources "ram=30" -j 2 data/assertions/assertions.csv combine_assertions ^~/results/assertions_build.txt
