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
if not test -d /srv/formulas/postgres-formula
    git clone https://github.com/saltstack-formulas/postgres-formula /srv/formulas/postgres-formula
end

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

echo "Applying SaltStack state (this could take minutes to complete)"
salt '*' state.apply

cp -a (pwd) /home/conceptnet/

echo "Swithing to conceptnet user and running all rules"
sudo -u conceptnet /home/conceptnet/conceptnet_rocks_virtualenv/bin/snakemake --snakefile /home/conceptnet/conceptnet-benchmark/Snakefile -j1
