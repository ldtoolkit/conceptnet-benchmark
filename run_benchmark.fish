#!/usr/bin/env fish

set library $argv[1]
if not set -q argv[1]
  echo "Library should be set (conceptnet5|conceptnet_rocks)"
  exit 1
end

/home/conceptnet/conceptnet_rocks_virtualenv/bin/python /home/conceptnet/conceptnet_rocks_virtualenv/bin/conceptnet-rocks start-arangodb &

while not /home/conceptnet/conceptnet_rocks_virtualenv/bin/python /home/conceptnet/conceptnet_rocks_virtualenv/bin/conceptnet-rocks is-arangodb-running
  sleep 0.1
end

for what in node relation source dataset edge_uri
  echo "Processing $what"
  "/home/conceptnet/"$library"_virtualenv/bin/python" /home/conceptnet/conceptnet-benchmark/system_requirements.py "/home/conceptnet/"$library"_virtualenv/bin/python" /home/conceptnet/conceptnet-benchmark/benchmark.py /home/conceptnet/benchmark_data/random_$what.csv $library >"/home/conceptnet/results/"$library"_"$what"_time_profile.txt" ^"/home/conceptnet/results/"$library"_"$what"_profile.txt"
end

/home/conceptnet/conceptnet_rocks_virtualenv/bin/python /home/conceptnet/conceptnet_rocks_virtualenv/bin/conceptnet-rocks stop-arangodb
