#!/usr/bin/env python3
from ast import literal_eval
from pathlib import Path
import csv
from timeit import timeit
from typing import List

import typer

from conceptnet5.db.query import AssertionFinder
from conceptnet5.nodes import standardized_concept_uri


def query(concepts: List[str]):
    af = AssertionFinder()
    for concept in concepts:
        _ = af.lookup(concept, limit=None)


def main(database_path_hint: Path, csv_dir: Path):
    csv_file_path = csv_dir.expanduser() / "random_concepts.csv"
    with open(str(csv_file_path), newline="") as f:
        reader = csv.DictReader(f)
        concepts = []
        for row in reader:
            concept = row
            concept["sense"] = literal_eval(concept["sense"])
            concepts.append(standardized_concept_uri(concept["language"], concept["label"], *concept["sense"]))
    print(timeit("query(concepts)", number=1, globals={**globals(), **locals()}))


if __name__ == "__main__":
    typer.run(main)
