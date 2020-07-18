#!/usr/bin/env python3
from ast import literal_eval
from pathlib import Path
from timeit import timeit
from typing import List
import csv

import typer

from conceptnet5.db.query import AssertionFinder
from conceptnet5.nodes import standardized_concept_uri


def query(af: AssertionFinder, concepts: List[str]):
    for concept in concepts:
        _ = af.lookup(concept, limit=None)


def read_concepts_from_csv(path: Path) -> List[str]:
    with open(str(path), newline="") as f:
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
    return concepts


def profile(csv_path: Path):
    af = AssertionFinder()
    concepts = read_concepts_from_csv(csv_path.expanduser())
    vars_to_pass = {"query": query, "af": af, "concepts": concepts}
    return timeit("query(af, concepts)", number=1, globals=vars_to_pass)


def main(csv_path: Path):
    print(profile(csv_path=csv_path))


if __name__ == "__main__":
    typer.run(main)
