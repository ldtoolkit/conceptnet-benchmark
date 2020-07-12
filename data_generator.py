#!/usr/bin/env python3
from pathlib import Path
from typing import Optional
import csv

from tqdm import tqdm
import dask.dataframe as dd
import typer

from lightning_conceptnet import LightningConceptNet


def main(database_path_hint: Path, output_dir: Path, count: Optional[int] = None):
    lcn = LightningConceptNet(database_path_hint)
    csv_file_path = output_dir / "concepts.csv"
    if not csv_file_path.is_file():
        with open(str(csv_file_path), "w", newline="") as f:
            concept = next(iter(lcn.concept))
            fields_to_skip = ["oid", "external_url"]
            field_names = [key for key in concept.to_dict().keys() if key not in fields_to_skip]
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()
            rows = []
            print("Writing concepts from database into CSV:")
            total = lcn._db.node_table.records()
            chunk_size = 1_000_000
            for i, concept in tqdm(enumerate(lcn.concept), unit=" concepts", unit_scale=True, total=total):
                d = concept.to_dict()
                for field in fields_to_skip:
                    del d[field]
                rows.append(d)
                if len(rows) == chunk_size:
                    writer.writerows(rows)
                    rows = []
            writer.writerows(rows)
    else:
        print(f"File exists, skipping creation: {csv_file_path}")
    random_csv_file_path = output_dir / "random_concepts.csv"
    if not random_csv_file_path.is_file():
        print("Read concepts from CSV into dask DataFrame")
        df = dd.read_csv(csv_file_path, keep_default_na=False)
        if count is None:
            frac = 1.0
        else:
            frac = count / len(df.index)
        print("Writing random concepts from dask DataFrame into CSV")
        df.sample(frac=frac).to_csv(str(random_csv_file_path), index=None, single_file=True)
    else:
        print(f"File exists, skipping creation: {random_csv_file_path}")


if __name__ == "__main__":
    typer.run(main)
