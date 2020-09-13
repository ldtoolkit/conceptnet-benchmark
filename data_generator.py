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
            print("Writing items from database into CSV:")
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
        print("Read items from CSV into dask DataFrame")
        df = dd.read_csv(all_nodes_file_path, keep_default_na=False)
        if count is None:
            frac = 1.0
        else:
            frac = count / len(df.index)
        print("Writing random items from dask DataFrame into CSV")
        df.sample(frac=frac).to_csv(str(random_nodes_file_path), index=None, single_file=True)
    else:
        print(f"File exists, skipping creation: {random_nodes_file_path}")


if __name__ == "__main__":
    app()
