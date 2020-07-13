#!/usr/bin/env python3
from ast import literal_eval
from pathlib import Path
import csv
from timeit import timeit
from typing import List

import typer

from conceptnet5.db.query import AssertionFinder
from conceptnet5.nodes import standardized_concept_uri


def query(af: AssertionFinder, concepts: List[str]):
    for concept in concepts:
        _ = af.lookup(concept, limit=None)


def main(csv_path: Path):
    csv_file_path = csv_path.expanduser()
    with open(str(csv_file_path), newline="") as f:
        reader = csv.DictReader(f)
        concepts = []
        for row in reader:
            concept = row
            language = concept["language"]
            text = concept.get("label")
            if text:
                sense = literal_eval(concept.get("sense")) or []
                concepts.append(standardized_concept_uri(language, text, *sense))
            else:
                concepts.append(f"/c/{language}")
    af = AssertionFinder()
    print(timeit("query(af, concepts)", number=1, globals={**globals(), **locals()}))


if __name__ == "__main__":
    typer.run(main)
