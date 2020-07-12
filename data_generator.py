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
    with open(str(csv_file_path), "w", newline="") as f:
        concept = next(iter(lcn.concept))
        fields_to_skip = ["oid", "external_url"]
        writer = csv.DictWriter(f, fieldnames=[key for key in concept.to_dict().keys() if key not in fields_to_skip])
        writer.writeheader()
        for i, concept in tqdm(enumerate(lcn.concept), total=lcn._db.node_table.records()):
            d = concept.to_dict()
            for field in fields_to_skip:
                del d[field]
            writer.writerow(d)
    df = dd.read_csv(csv_file_path)
    random_csv_file_path = output_dir / "random_concepts.csv"
    if count is None:
        frac = 1.0
    else:
        frac = count / len(df.index)
    df.sample(frac=frac).to_csv(str(random_csv_file_path), index=None, single_file=True)


if __name__ == "__main__":
    typer.run(main)
