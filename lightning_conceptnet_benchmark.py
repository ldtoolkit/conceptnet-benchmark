#!/usr/bin/env python3
from ast import literal_eval
from pathlib import Path
import csv
from timeit import timeit
from typing import Dict, List

import typer

from lightning_conceptnet import LightningConceptNet


def query(database_path_hint: Path, concepts: List[Dict]):
    lcn = LightningConceptNet(database_path_hint)
    with lcn.read_transaction as txn:
        for concept in concepts:
            _ = list(lcn.concept(txn=txn).has(**concept).edge_all())


def main(database_path_hint: Path, csv_dir: Path):
    csv_file_path = csv_dir.expanduser() / "random_concepts.csv"
    with open(str(csv_file_path), newline="") as f:
        reader = csv.DictReader(f)
        concepts = []
        for row in reader:
            concept = row
            concept["sense"] = literal_eval(concept["sense"])
            concepts.append(concept)
    print(timeit("query(database_path_hint, concepts)", number=1, globals={**globals(), **locals()}))


if __name__ == "__main__":
    typer.run(main)
