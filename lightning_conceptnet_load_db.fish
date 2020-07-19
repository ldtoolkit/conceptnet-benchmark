#!/usr/bin/env fish

set BASEDIR (dirname (status --current-filename))

echo "Activating virtualenv"
source ~/lightning_conceptnet-virtualenv/bin/activate.fish

echo "Loading ConceptNet into Lightning ConceptNet database (LMDB)"
$BASEDIR/system_requirements.py lightning-conceptnet-build ~/conceptnet.db ~/conceptnet5/data/assertions.csv ^~/results/lightning_conceptnet_load_db.txt
