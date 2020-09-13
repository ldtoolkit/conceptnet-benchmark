arangodb_install_dir = "/home/conceptnet/.arangodb"
arangodb_data_dir = f"{arangodb_install_dir}/data"
arangodb_exe = f"{arangodb_install_dir}/bin/arangodb"
conceptnet5_dir = "/home/conceptnet/conceptnet5"
conceptnet5_virtualenv = "/home/conceptnet/conceptnet5_virtualenv"
conceptnet5_postgresql_done = f"{conceptnet5_dir}/data/psql/done"
conceptnet5_python = f"{conceptnet5_virtualenv}/bin/python"
conceptnet5_snakemake = f"{conceptnet5_virtualenv}/bin/snakemake"
conceptnet_benchmark_dir = "/home/conceptnet/conceptnet-benchmark"
conceptnet_rocks_virtualenv = "/home/conceptnet/conceptnet_rocks_virtualenv"
conceptnet_rocks_python = f"{conceptnet_rocks_virtualenv}/bin/python"
conceptnet_rocks = f"{conceptnet_rocks_virtualenv}/bin/conceptnet-rocks"
edge_count = f"--edge-count {config['edge_count']}" if config.get('edge_count') else ""
results_dir = "/home/conceptnet/results"
system_requirements = f"{conceptnet_benchmark_dir}/system_requirements.py"
assertions_file = f"{conceptnet5_dir}/data/assertions.csv"
assertions_msgpack_file = f"{conceptnet5_dir}/data/assertions/assertions.msgpack"

rule all:
  input:
    assertions_file,
    assertions_msgpack_file,
    conceptnet5_postgresql_done,
    arangodb_data_dir

rule prepare_assertions:
  output:
    assertions_file,
    assertions_msgpack_file
  shell:
    "{conceptnet5_python} {system_requirements} {conceptnet5_snakemake} --snakefile {conceptnet5_dir}/Snakefile --resources 'ram=30' -j1 combine_assertions data/assertions/assertions.csv 2>{results_dir}/assertions_build.txt"

rule load_conceptnet5_database:
  input:
    assertions_msgpack_file
  output:
    conceptnet5_postgresql_done
  shell:
    "{conceptnet5_python} {system_requirements} {conceptnet5_snakemake} --snakefile {conceptnet5_dir}/Snakefile --resources 'ram=30' -j1 load_db 2>{results_dir}/conceptnet5_load_db.txt"

rule install_arangodb:
  output:
    directory(arangodb_install_dir),
    arangodb_exe
  shell:
    "{conceptnet_rocks} install-arangodb"

rule load_conceptnet_rocks_database:
  input:
    arangodb_exe
  output:
    directory(arangodb_data_dir)
  shell:
    "{conceptnet_rocks_python} {system_requirements} {conceptnet_rocks} load {assertions_file} {edge_count} 2>{results_dir}/conceptnet_rocks_load_db.txt"
