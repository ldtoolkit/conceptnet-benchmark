#!/usr/bin/env sh
systemctl stop postgresql
sync
echo 3 > /proc/sys/vm/drop_caches
systemctl start postgresql
