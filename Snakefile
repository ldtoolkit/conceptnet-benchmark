arangodb_install_dir = "/home/conceptnet/.arangodb"
arangodb_data_dir = f"{arangodb_install_dir}/data"
arangodb_exe = f"{arangodb_install_dir}/bin/arangodb"
benchmark_data_dir = "/home/conceptnet/benchmark_data"
conceptnet5_dir = "/home/conceptnet/conceptnet5"
conceptnet5_virtualenv = "/home/conceptnet/conceptnet5_virtualenv"
conceptnet5_postgresql_done = f"{conceptnet5_dir}/data/psql/done"
conceptnet5_python = f"{conceptnet5_virtualenv}/bin/python"
conceptnet5_snakemake = f"{conceptnet5_virtualenv}/bin/snakemake"
conceptnet_benchmark_dir = "/home/conceptnet/conceptnet-benchmark"
conceptnet_benchmark_exe = f"{conceptnet_benchmark_dir}/benchmark.py"
conceptnet_benchmark_data_generator = f"{conceptnet_benchmark_dir}/data_generator.py"
conceptnet_benchmark_tables_generator = f"{conceptnet_benchmark_dir}/generate_tables.py"
conceptnet_rocks_virtualenv = "/home/conceptnet/conceptnet_rocks_virtualenv"
conceptnet_rocks_python = f"{conceptnet_rocks_virtualenv}/bin/python"
conceptnet_rocks_exe = f"{conceptnet_rocks_virtualenv}/bin/conceptnet-rocks"
edge_count = f"--edge-count {config['edge_count']}" if config.get('edge_count') else ""
generate_data_exe = f"{conceptnet_benchmark_dir}/generate_data.fish"
results_dir = "/home/conceptnet/results"
system_requirements = f"{conceptnet_benchmark_dir}/system_requirements.py"
assertions_file = f"{conceptnet5_dir}/data/assertions.csv"
assertions_msgpack_file = f"{conceptnet5_dir}/data/assertions/assertions.msgpack"
benchmark_exe = f"{conceptnet_benchmark_dir}/run_benchmark.fish"

rule all:
  input:
    assertions_file,
    assertions_msgpack_file,
    conceptnet5_postgresql_done,
    arangodb_data_dir,
    f"{results_dir}/conceptnet5_node_profile.txt",
    f"{results_dir}/conceptnet5_relation_profile.txt",
    f"{results_dir}/conceptnet5_source_profile.txt",
    f"{results_dir}/conceptnet5_dataset_profile.txt",
    f"{results_dir}/conceptnet5_edge_uri_profile.txt",
    f"{results_dir}/conceptnet_rocks_node_profile.txt",
    f"{results_dir}/conceptnet_rocks_relation_profile.txt",
    f"{results_dir}/conceptnet_rocks_source_profile.txt",
    f"{results_dir}/conceptnet_rocks_dataset_profile.txt",
    f"{results_dir}/conceptnet_rocks_edge_uri_profile.txt"

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
    conceptnet5_postgresql_done,
    f"{results_dir}/conceptnet5_load_db.txt"
  shell:
    "{conceptnet5_python} {system_requirements} {conceptnet5_snakemake} --snakefile {conceptnet5_dir}/Snakefile --resources 'ram=30' -j1 load_db 2>{results_dir}/conceptnet5_load_db.txt"

rule install_arangodb:
  output:
    directory(arangodb_install_dir)
  shell:
    "{conceptnet_rocks_python} {conceptnet_rocks_exe} install-arangodb"

rule load_conceptnet_rocks_database:
  input:
    assertions_file,
    arangodb_exe
  output:
    directory(arangodb_data_dir),
    f"{results_dir}/conceptnet_rocks_load_db.txt"
  shell:
    "{conceptnet_rocks_python} {system_requirements} {conceptnet_rocks_exe} load {assertions_file} {edge_count} 2>{results_dir}/conceptnet_rocks_load_db.txt"

rule generate_random_data:
  input:
    arangodb_data_dir
  output:
    directory(benchmark_data_dir),
    f"{benchmark_data_dir}/random_node.csv",
    f"{benchmark_data_dir}/random_relation.csv",
    f"{benchmark_data_dir}/random_source.csv",
    f"{benchmark_data_dir}/random_dataset.csv",
    f"{benchmark_data_dir}/random_edge_uri.csv"
  shell:
    generate_data_exe

rule benchmark_conceptnet5:
  input:
    f"{benchmark_data_dir}/random_node.csv",
    f"{benchmark_data_dir}/random_relation.csv",
    f"{benchmark_data_dir}/random_source.csv",
    f"{benchmark_data_dir}/random_dataset.csv",
    f"{benchmark_data_dir}/random_edge_uri.csv"
  output:
    f"{results_dir}/conceptnet5_node_profile.txt",
    f"{results_dir}/conceptnet5_relation_profile.txt",
    f"{results_dir}/conceptnet5_source_profile.txt",
    f"{results_dir}/conceptnet5_dataset_profile.txt",
    f"{results_dir}/conceptnet5_edge_uri_profile.txt"
  shell:
    "{benchmark_exe} conceptnet5"

rule benchmark_conceptnet_rocks:
  input:
    f"{benchmark_data_dir}/random_node.csv",
    f"{benchmark_data_dir}/random_relation.csv",
    f"{benchmark_data_dir}/random_source.csv",
    f"{benchmark_data_dir}/random_dataset.csv",
    f"{benchmark_data_dir}/random_edge_uri.csv"
  output:
    f"{results_dir}/conceptnet_rocks_node_profile.txt",
    f"{results_dir}/conceptnet_rocks_relation_profile.txt",
    f"{results_dir}/conceptnet_rocks_source_profile.txt",
    f"{results_dir}/conceptnet_rocks_dataset_profile.txt",
    f"{results_dir}/conceptnet_rocks_edge_uri_profile.txt"
  shell:
    "{benchmark_exe} conceptnet_rocks"

rule generate_tables:
  input:
    f"{results_dir}/conceptnet5_load_db.txt",
    f"{results_dir}/conceptnet_rocks_load_db.txt",
    f"{results_dir}/conceptnet5_node_profile.txt",
    f"{results_dir}/conceptnet5_relation_profile.txt",
    f"{results_dir}/conceptnet5_source_profile.txt",
    f"{results_dir}/conceptnet5_dataset_profile.txt",
    f"{results_dir}/conceptnet5_edge_uri_profile.txt",
    f"{results_dir}/conceptnet_rocks_node_profile.txt",
    f"{results_dir}/conceptnet_rocks_relation_profile.txt",
    f"{results_dir}/conceptnet_rocks_source_profile.txt",
    f"{results_dir}/conceptnet_rocks_dataset_profile.txt",
    f"{results_dir}/conceptnet_rocks_edge_uri_profile.txt"
  output:
    f"{results_dir}/Load database time.md",
    f"{results_dir}/Load database RAM.md",
    f"{results_dir}/Load database disk.md",
    f"{results_dir}/Query time.md",
    f"{results_dir}/Query RAM.md",
    f"{results_dir}/Query disk.md"
  shell:
    "{conceptnet_rocks_python} {conceptnet_benchmark_tables_generator}"
