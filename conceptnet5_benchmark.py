#!/usr/bin/env python3
from ast import literal_eval
from pathlib import Path
from timeit import timeit
from typing import List
import csv

import typer

from conceptnet5.db.query import AssertionFinder
from conceptnet5.nodes import standardized_concept_uri


def query(af: AssertionFinder, concepts: List[str], query_external_urls: bool, verbose: bool = False):
    assertion_count = 0
    external_url_count = 0
    assertions_strs = []
    external_urls_strs = []

    for concept in concepts:
        edges = af.lookup(concept, limit=None)
        assertions = [edge for edge in edges if edge["rel"]["label"] != "ExternalURL"]
        if query_external_urls:
            external_urls = [edge["end"]["term"] for edge in edges if edge["rel"]["label"] == "ExternalURL"]
            if verbose:
                external_urls_strs.extend(external_urls)
                external_url_count += len(external_urls)
        if verbose:
            assertions_strs.extend(
                f"{assertion['rel']['label']}: {assertion['start']['@id']} - {assertion['end']['@id']}"
                for assertion in assertions
            )
            assertion_count += len(assertions)

    if verbose:
        print("Assertions:")
        for assertion_str in sorted(assertions_strs):
            print(assertion_str)
        print(f"Assertion count: {assertion_count}")
        print(f"External URLs:")
        for external_url_str in sorted(external_urls_strs):
            print(external_url_str)
        print(f"External URL count: {external_url_count}")


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


def profile(csv_path: Path, query_external_urls: bool, verbose: bool):
    af = AssertionFinder()
    concepts = read_concepts_from_csv(csv_path.expanduser())
    vars_to_pass = {
        "query": query,
        "af": af,
        "concepts": concepts,
        "query_external_urls": query_external_urls,
        "verbose": verbose,
    }
    return timeit(
        """query(
            af=af,
            concepts=concepts,
            query_external_urls=query_external_urls,
            verbose=verbose,
        )""",
        number=1,
        globals=vars_to_pass,
    )


def main(csv_path: Path, query_external_urls: bool = False, verbose: bool = False):
    print(profile(csv_path=csv_path, query_external_urls=query_external_urls, verbose=verbose))


if __name__ == "__main__":
    typer.run(main)
