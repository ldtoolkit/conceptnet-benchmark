#!/usr/bin/env python3
from ast import literal_eval
from itertools import chain
from pathlib import Path
from timeit import timeit
from typing import Dict, List, Any
import csv

import typer

from lightning_conceptnet import LightningConceptNet


def query(lcn: LightningConceptNet, concepts: List[Dict[str, Any]], query_external_urls: bool, verbose: bool):
    assertion_count = 0
    external_url_count = 0
    assertions_strs = []
    external_urls_strs = []

    with lcn.read_transaction as txn:
        for concept in concepts:
            assertions = list(lcn.concept(txn=txn).has(**concept).edge_all())
            if query_external_urls:
                external_urls = list(chain(*(
                    concept_out.external_url for concept_out in lcn.concept(txn=txn).has(**concept)
                    if concept_out.external_url is not None
                )))
                if verbose:
                    external_urls_strs.extend(external_urls)
                    external_url_count += len(external_urls)
            if verbose:
                assertions_strs.extend(
                    f"{assertion.relation}: {assertion.start.uri} - {assertion.end.uri}"
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


def profile(database_path_hint: Path, csv_path: Path, query_external_urls: bool, verbose: bool):
    lcn = LightningConceptNet(database_path_hint)
    concepts = read_concepts_from_csv(csv_path.expanduser())
    vars_to_pass = {
        "query": query,
        "lcn": lcn,
        "concepts": concepts,
        "query_external_urls": query_external_urls,
        "verbose": verbose,
    }
    return timeit(
        """query(
               lcn=lcn,
               concepts=concepts,
               query_external_urls=query_external_urls,
               verbose=verbose,
           )""",
        number=1,
        globals=vars_to_pass,
    )


def main(database_path_hint: Path, csv_path: Path, query_external_urls: bool = False, verbose: bool = False):
    print(profile(
        database_path_hint=database_path_hint,
        csv_path=csv_path,
        query_external_urls=query_external_urls,
        verbose=verbose,
    ))


if __name__ == "__main__":
    typer.run(main)
