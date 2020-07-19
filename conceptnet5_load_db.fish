#!/usr/bin/env fish

set BASEDIR (dirname (status --current-filename))

echo "Activating virtualenv"
source ~/conceptnet5-virtualenv/bin/activate.fish

echo "Changing the directory to conceptnet5 repo"
cd ~/conceptnet5

echo "Loading ConceptNet into ConceptNet5 database (PostgreSQL)"
$BASEDIR/system_requirements.py snakemake --resources "ram=30" -j 2 load_db ^~/results/conceptnet5_load_db.txt
