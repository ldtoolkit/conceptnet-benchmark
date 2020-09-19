# ConceptNet Benchmark

This repository contains code to setup [ConceptNet5](https://github.com/commonsense/conceptnet5) and [ConceptNet Rocks](https://github.com/ldtoolkit/conceptnet-rocks), create the databases from dumps, and run the benchmarks.

## Usage

Benchmarks are supposed to be run on a clean Ubuntu 20.04.1. We used VM on [Digital Ocean](https://www.digitalocean.com/) with following plan: General Purpose, $520/mo, 64 GB / 16 CPU, 400 GB SSD disk, 7 TB transfer.

To start the benchmark just download this repository and run `run.sh`:

```bash
sudo apt install unzip wget
wget https://github.com/ldtoolkit/conceptnet-benchmark/archive/master.zip
unzip master.zip
cd conceptnet-benchmark-master/
sudo bash run.sh
```

After a few hours you will get the results in `~conceptnet/results` folder.