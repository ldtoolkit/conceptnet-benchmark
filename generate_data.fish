#!/usr/bin/env fish

/home/conceptnet/conceptnet_rocks_virtualenv/bin/python /home/conceptnet/conceptnet_rocks_virtualenv/bin/conceptnet-rocks start-arangodb &

while not /home/conceptnet/conceptnet_rocks_virtualenv/bin/python /home/conceptnet/conceptnet_rocks_virtualenv/bin/conceptnet-rocks is-arangodb-running
  sleep 0.1
end

/home/conceptnet/conceptnet_rocks_virtualenv/bin/python /home/conceptnet/conceptnet-benchmark/data_generator.py node relation source dataset edge_uri /home/conceptnet/benchmark_data --count 10000 --source-count 10

/home/conceptnet/conceptnet_rocks_virtualenv/bin/python /home/conceptnet/conceptnet_rocks_virtualenv/bin/conceptnet-rocks stop-arangodb
