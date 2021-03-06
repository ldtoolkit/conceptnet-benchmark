#!/usr/bin/env python3
from arango import ArangoClient
from conceptnet_rocks import arangodb
from conceptnet_rocks.database import DEFAULT_DATABASE
from enum import Enum
from pathlib import Path
from typing import Optional, List
import dask.dataframe as dd
import typer


class What(Enum):
    node = "node"
    relation = "relation"
    source = "source"
    dataset = "dataset"
    edge_uri = "edge_uri"


app = typer.Typer()


AQLS = {
    What.node: """
        for node in nodes 
          return distinct rtrim(node.uri, "/")
    """,
    What.relation: """
        for edge in edges
          return distinct edge.rel
    """,
    What.source: """
        for edge in edges
          for source in edge.sources
            for value in values(source)
              return distinct rtrim(value, "/")
    """,
    What.dataset: """
        for edge in edges
          return distinct rtrim(edge.dataset, "/")
    """,
    What.edge_uri: """
        for edge in edges
          return distinct edge.uri
    """,
}


def generate_one(
        what: What,
        output_dir: Path,
        count: Optional[int] = None,
        connection_uri: str = arangodb.DEFAULT_CONNECTION_URI,
        database: str = DEFAULT_DATABASE,
        root_password: str = arangodb.DEFAULT_ROOT_PASSWORD,
        arangodb_exe_path: Path = arangodb.DEFAULT_INSTALL_PATH,
        data_path: Path = arangodb.DEFAULT_DATA_PATH,
):
    print(f"Processing {what.value}")

    output_dir = output_dir.expanduser()
    all_items_file_path = output_dir / f"{what.value}.csv"

    if not all_items_file_path.is_file():
        with open(str(all_items_file_path), "w") as f:
            print("Writing items from database into CSV")
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
                cursor = db.aql.execute(AQLS[what], batch_size=batch_size)
                lines = []
                for uri in cursor:
                    lines.append(f"{uri}\n")
                    if len(lines) == batch_size:
                        f.writelines(lines)
                        lines = []
                f.writelines(lines)
    else:
        print(f"File exists, skipping creation: {all_items_file_path}")

    random_items_file_path = output_dir / f"random_{what.value}.csv"
    if not random_items_file_path.is_file():
        print("Read items from CSV into dask DataFrame")
        df = dd.read_csv(all_items_file_path, sep="\t", keep_default_na=False)
        if count is None:
            frac = 1.0
        else:
            frac = min(1.0, count / len(df.index))
        print("Writing random items from dask DataFrame into CSV")
        df.sample(frac=frac, random_state=42).to_csv(str(random_items_file_path), index=None, single_file=True)
    else:
        print(f"File exists, skipping creation: {random_items_file_path}")


@app.command()
def generate(
        what: List[What],
        output_dir: Path,
        count: Optional[int] = None,
        node_count: Optional[int] = None,
        relation_count: Optional[int] = None,
        source_count: Optional[int] = None,
        dataset_count: Optional[int] = None,
        edge_uri_count: Optional[int] = None,
        connection_uri: str = arangodb.DEFAULT_CONNECTION_URI,
        database: str = DEFAULT_DATABASE,
        root_password: str = arangodb.DEFAULT_ROOT_PASSWORD,
        arangodb_exe_path: Path = arangodb.DEFAULT_INSTALL_PATH,
        data_path: Path = arangodb.DEFAULT_DATA_PATH,
):
    for x in what:
        x_count = {
            What.node: node_count,
            What.relation: relation_count,
            What.source: source_count,
            What.dataset: dataset_count,
            What.edge_uri: edge_uri_count,
        }[x] or count
        generate_one(
            what=x,
            output_dir=output_dir,
            count=x_count,
            connection_uri=connection_uri,
            database=database,
            root_password=root_password,
            arangodb_exe_path=arangodb_exe_path,
            data_path=data_path,
        )


if __name__ == "__main__":
    app()
