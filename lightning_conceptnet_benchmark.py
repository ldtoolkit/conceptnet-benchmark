#!/usr/bin/env python3
from ast import literal_eval
from pathlib import Path
import csv
from timeit import timeit
from typing import Dict, List

import typer

from lightning_conceptnet import LightningConceptNet


def query(lcn: LightningConceptNet, concepts: List[Dict]):
    with lcn.read_transaction as txn:
        for concept in concepts:
            _ = list(lcn.concept(txn=txn).has(**concept).edge_all())


def main(database_path_hint: Path, csv_path: Path):
    csv_file_path = csv_path.expanduser()
    with open(str(csv_file_path), newline="") as f:
        reader = csv.DictReader(f)
        concepts = []
        for row in reader:
            concept = row
            if "label" in concept and not concept["label"]:
                del concept["label"]
            if "sense" in concept and not literal_eval(concept["sense"]):
                del concept["sense"]
            concepts.append(concept)
    lcn = LightningConceptNet(database_path_hint)
    print(timeit("query(lcn, concepts)", number=1, globals={**globals(), **locals()}))


if __name__ == "__main__":
    typer.run(main)
