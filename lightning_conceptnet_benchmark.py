#!/usr/bin/env python3
from ast import literal_eval
from pathlib import Path
from timeit import timeit
from typing import Dict, List, Any
import csv

import typer

from lightning_conceptnet import LightningConceptNet


def query(lcn: LightningConceptNet, concepts: List[Dict[str, Any]], query_concepts: bool):
    with lcn.read_transaction as txn:
        for concept in concepts:
            _ = list(lcn.concept(txn=txn).has(**concept).edge_all())
            if query_concepts:
                _ = list(lcn.concept(txn=txn).has(**concept))


def read_concepts_from_csv(path: Path) -> List[Dict[str, Any]]:
    with open(str(path), newline="") as f:
        reader = csv.DictReader(f)
        concepts = []
        for row in reader:
            concept = row
            if "label" in concept and not concept["label"]:
                del concept["label"]
            if "sense" in concept:
                concept["sense"] = literal_eval(concept["sense"])
                if not concept["sense"]:
                    del concept["sense"]
            concepts.append(concept)
    return concepts


def profile(database_path_hint: Path, csv_path: Path, query_concepts: bool):
    lcn = LightningConceptNet(database_path_hint)
    concepts = read_concepts_from_csv(csv_path.expanduser())
    vars_to_pass = {"query": query, "lcn": lcn, "concepts": concepts, "query_concepts": query_concepts}
    return timeit("query(lcn, concepts, query_concepts)", number=1, globals=vars_to_pass)


def main(database_path_hint: Path, csv_path: Path, query_concepts: bool = False):
    print(profile(database_path_hint=database_path_hint, csv_path=csv_path, query_concepts=query_concepts))


if __name__ == "__main__":
    typer.run(main)
