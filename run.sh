#!/usr/bin/env sh

echo "This script will install ConceptNet5 and ConceptNet Rocks and run the benchmarks."
echo
echo "Software requirements: Ubuntu Server 20.04.1"
echo "Hardware requirements: https://github.com/commonsense/conceptnet5/wiki/Build-process"
echo
echo "==========================================================================================="
echo "= This script will change your OS! Do not run it on a computer you use for anything else! ="
echo "==========================================================================================="
echo
while true; do
    read -p "Do you wish to continue [yes/no]? " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

is_user_root() { [ "$(id -u)" -eq 0 ]; }

if is_user_root; then
  echo "Checking root permissions... OK"
else
  echo "Checking root permissions... Please run this script as root"
  exit 1
fi

echo "Starting the installation"
echo
echo "Installing fish shell to continue the installation process"

apt install --assume-yes fish

BASEDIR=$(dirname "$0")

fish "$BASEDIR/run.fish"
