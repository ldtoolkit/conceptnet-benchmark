#!/usr/bin/env fish
set BASEDIR (dirname (status --current-filename))

echo "Installing git"

apt install --assume-yes git

mkdir -p /srv/salt
cp $BASEDIR/salt/states/* /srv/salt/
cp -r $BASEDIR/requirements /srv/salt/

mkdir -p /srv/pillar
cp $BASEDIR/salt/pillar/* /srv/pillar/

mkdir -p /srv/formulas
git clone https://github.com/saltstack-formulas/postgres-formula /srv/formulas/postgres-formula

echo "Installing SaltStack"

curl -o bootstrap-salt.sh -L https://bootstrap.saltstack.com

set minion_config '{"master": "localhost"}'
set master_config (echo '
{
    "auto_accept": true, 
    "file_roots": {
        "base": [
            "/srv/salt",
            "/srv/formulas/postgres-formula"
        ]
    },
    "interface": "127.0.0.1"
}
')

sh bootstrap-salt.sh -M -j "$minion_config" -J "$master_config"

while not salt '*' test.ping >/dev/null ^/dev/null
  echo "Waiting for SaltStack startup"
  sleep 1
end

echo "Applying SaltStack state"
salt '*' state.apply

cp -a $BASEDIR/system_requirements.py ~conceptnet/
cp -a $BASEDIR/prepare_assertions.fish ~conceptnet/
cp -a $BASEDIR/conceptnet5_load_db.fish ~conceptnet/
cp -a $BASEDIR/lightning_conceptnet_load_db.fish ~conceptnet/
chown conceptnet:conceptnet -R ~conceptnet

# echo "Swithing to conceptnet user and preparing assertions"
# sudo -u conceptnet /home/conceptnet/prepare_assertions.fish
# 
# echo "Swithing to conceptnet user and loading ConceptNet5 database"
# sudo -u conceptnet /home/conceptnet/conceptnet5_load_db.fish

echo "Swithing to conceptnet user and loading Lightning ConceptNet database"
sudo -u conceptnet /home/conceptnet/lightning_conceptnet_load_db.fish
