#!/usr/bin/env python3
from pathlib import Path
from typing import Optional

from tqdm import tqdm
import typer


app = typer.Typer()


@app.command()
def concepts(database_path_hint: Path, output_dir: Path, count: Optional[int] = None):
    from lightning_conceptnet import LightningConceptNet
    import csv
    import dask.dataframe as dd

    database_path_hint = database_path_hint.expanduser()
    output_dir = output_dir.expanduser()
    lcn = LightningConceptNet(database_path_hint)
    csv_file_path = output_dir / "concepts.csv"
    if not csv_file_path.is_file():
        with open(str(csv_file_path), "w", newline="") as f:
            with lcn.read_transaction as txn:
                concept = next(iter(lcn.concept(txn)))
                fields_to_skip = ["oid", "external_url"]
                field_names = [key for key in concept.to_dict().keys() if key not in fields_to_skip]
                writer = csv.DictWriter(f, fieldnames=field_names)
                writer.writeheader()
                rows = []
                print("Writing concepts from database into CSV:")
                total = lcn._db.node_table.records()
                chunk_size = 1_000_000
                for i, concept in tqdm(enumerate(lcn.concept(txn)), unit=" concepts", unit_scale=True, total=total):
                    d = concept.to_dict()
                    for field in fields_to_skip:
                        del d[field]
                    rows.append(d)
                    if len(rows) == chunk_size:
                        writer.writerows(rows)
                        rows = []
                writer.writerows(rows)
    else:
        print(f"File exists, skipping creation: {csv_file_path}")
    random_csv_file_path = output_dir / "random_concepts.csv"
    if not random_csv_file_path.is_file():
        print("Read concepts from CSV into dask DataFrame")
        df = dd.read_csv(csv_file_path, keep_default_na=False)
        if count is None:
            frac = 1.0
        else:
            frac = count / len(df.index)
        print("Writing random concepts from dask DataFrame into CSV")
        df.sample(frac=frac).to_csv(str(random_csv_file_path), index=None, single_file=True)
    else:
        print(f"File exists, skipping creation: {random_csv_file_path}")


@app.command()
def all_languages(database_path_hint: Path, output_dir: Path):
    from lightning_conceptnet import LightningConceptNet

    database_path_hint = database_path_hint.expanduser()
    lcn = LightningConceptNet(database_path_hint)
    languages = set()
    total = lcn._db.node_table.records()
    print("Reading concepts from database to find all languages:")
    with lcn.read_transaction as txn:
        for i, concept in tqdm(enumerate(iter(lcn.concept(txn))), unit=" concepts", unit_scale=True, total=total):
            languages.add(concept.language)
    output_file_path = output_dir / "languages.txt"
    with open(str(output_file_path), "w") as f:
        for language in languages:
            f.write(f"{language}\n")


@app.command()
def languages(output_dir: Path):
    from conceptnet5.db.query import AssertionFinder

    af = AssertionFinder()

    input_file_path = output_dir / "languages.txt"
    output_file_path = output_dir / "small_languages.csv"
    with open(str(input_file_path)) as f_in:
        total = len(f_in.readlines())
    with open(str(input_file_path)) as f_in:
        with open(str(output_file_path), "w") as f_out:
            print("Writing small languages to CSV file:")
            f_out.write("language\n")
            for line in tqdm(f_in, total=total, unit=" languages"):
                language = line.strip()
                uri = f"/c/{language}"
                l = len(af.lookup(uri, limit=None))
                if l < 10_000:
                    f_out.write(line)


if __name__ == "__main__":
    app()
