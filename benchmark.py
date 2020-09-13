#!/usr/bin/env python3
from enum import Enum
from pathlib import Path
from timeit import timeit
import dask.dataframe as dd
import subprocess
import typer


class Library(Enum):
    conceptnet5 = "conceptnet5"
    conceptnet_rocks = "conceptnet_rocks"


LIMIT = 10000


def query(af, items: dd.DataFrame, verbose: bool = False):
    edge_count = 0
    edges_strs = []

    for item in items["uri"]:

        edges = af.lookup(item, limit=LIMIT)
        if verbose:
            edges_strs.extend(str(dict(sorted(edge.items()))) for edge in edges)
            edge_count += len(edges)

    if verbose:
        print("Edges:")
        for edge_str in sorted(edges_strs):
            print(edge_str)
        print(f"Edge count: {edge_count}")


def profile(csv_path: Path, library: Library, verbose: bool):
    if library == Library.conceptnet5:
        from conceptnet5.db.query import AssertionFinder
        script_dir = Path(__file__).resolve().parent
        subprocess.call(["sudo", script_dir / "postgresql_clear_cache.sh"])
        af = AssertionFinder()
    elif library == Library.conceptnet_rocks:
        from conceptnet_rocks import AssertionFinder
        af = AssertionFinder(close_stdout_and_stderr=True)
        af.clear_cache()
    else:
        raise ValueError(f"Unsupported library: {library}")

    items = dd.read_csv(csv_path.expanduser(), keep_default_na=False)
    vars_to_pass = {
        "query": query,
        "af": af,
        "items": items,
        "verbose": verbose,
    }
    return timeit(
        """query(
            af=af,
            items=items,
            verbose=verbose,
        )""",
        number=1,
        globals=vars_to_pass,
    )


def main(csv_path: Path, library: Library, verbose: bool = False, skip_profile: bool = False):
    profile_result = profile(csv_path=csv_path, library=library, verbose=verbose)
    if not skip_profile:
        print(profile_result)


if __name__ == "__main__":
    typer.run(main)
