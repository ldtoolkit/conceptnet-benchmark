#!/usr/bin/env python3
from arango import ArangoClient
from conceptnet_rocks import arangodb
from conceptnet_rocks.database import DEFAULT_DATABASE
from pathlib import Path
from tqdm import tqdm
from typing import Optional
import dask.dataframe as dd
import typer


app = typer.Typer()


@app.command()
def nodes(
        output_dir: Path,
        connection_uri: str = arangodb.DEFAULT_CONNECTION_URI,
        database: str = DEFAULT_DATABASE,
        root_password: str = arangodb.DEFAULT_ROOT_PASSWORD,
        arangodb_exe_path: Path = arangodb.DEFAULT_INSTALL_PATH,
        data_path: Path = arangodb.DEFAULT_DATA_PATH,
        count: Optional[int] = None,
):
    output_dir = output_dir.expanduser()
    all_nodes_file_path = output_dir / "nodes.csv"

    if not all_nodes_file_path.is_file():
        with open(str(all_nodes_file_path), "w") as f:
            print("Writing concepts from database into CSV:")
            f.write("uri\n")
            with arangodb.instance(
                    connection_uri=connection_uri,
                    root_password=root_password,
                    arangodb_exe_path=arangodb_exe_path,
                    data_path=data_path,
            ):
                client = ArangoClient(hosts=connection_uri)
                db = client.db(database)
                batch_size = 2**10
                cursor = db.aql.execute("FOR node IN nodes RETURN rtrim(node.uri, '/')", batch_size=batch_size)
                total = db.collection("nodes").count()
                lines = []
                for i, node_uri in tqdm(enumerate(cursor), unit=" nodes", unit_scale=True, total=total):
                    lines.append(f"{node_uri}\n")
                    if len(lines) == batch_size:
                        f.writelines(lines)
                        lines = []
                f.writelines(lines)
    else:
        print(f"File exists, skipping creation: {all_nodes_file_path}")

    random_nodes_file_path = output_dir / "random_nodes.csv"
    if not random_nodes_file_path.is_file():
        print("Read concepts from CSV into dask DataFrame")
        df = dd.read_csv(all_nodes_file_path, keep_default_na=False)
        if count is None:
            frac = 1.0
        else:
            frac = count / len(df.index)
        print("Writing random concepts from dask DataFrame into CSV")
        df.sample(frac=frac).to_csv(str(random_nodes_file_path), index=None, single_file=True)
    else:
        print(f"File exists, skipping creation: {random_nodes_file_path}")


@app.command()
def all_languages(database_path_hint: Path, output_dir: Path):
    from lightning_conceptnet import LightningConceptNet

    database_path_hint = database_path_hint.expanduser()
    lcn = LightningConceptNet(database_path_hint)
    languages = set()
    total = lcn._db.node_table.records()
    print("Reading concepts from database to find all languages:")
    with lcn.read_transaction as txn:
        for i, concept in tqdm(enumerate(iter(lcn.concept(txn))), unit=" concepts", unit_scale=True, total=total):
            languages.add(concept.language)
    output_file_path = output_dir / "languages.txt"
    with open(str(output_file_path), "w") as f:
        for language in languages:
            f.write(f"{language}\n")


@app.command()
def languages(output_dir: Path):
    from conceptnet5.db.query import AssertionFinder

    af = AssertionFinder()

    input_file_path = output_dir / "languages.txt"
    output_file_path = output_dir / "small_languages.csv"
    with open(str(input_file_path)) as f_in:
        total = len(f_in.readlines())
    with open(str(input_file_path)) as f_in:
        with open(str(output_file_path), "w") as f_out:
            print("Writing small languages to CSV file:")
            f_out.write("language\n")
            for line in tqdm(f_in, total=total, unit=" languages"):
                language = line.strip()
                uri = f"/c/{language}"
                l = len(af.lookup(uri, limit=None))
                if l < 10_000:
                    f_out.write(line)


if __name__ == "__main__":
    app()
