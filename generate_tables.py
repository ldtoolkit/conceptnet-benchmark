#!/usr/bin/env python3
from benchmark import Library
from benchmark import Library
from data_generator import What
from data_generator import What
from datetime import timedelta
from pathlib import Path
from pytablewriter import MarkdownTableWriter
import pandas as pd
import pytimeparse


results_dir = Path("/home/conceptnet/results")


def escape_underscore(s):
    return s.replace("_", "\\_")


def collect_load_db_data():
    time_dict = {}
    ram_dict = {}
    disk_dict = {}
    time_list = []
    ram_list = []
    disk_list = []
    for library in Library:
        with open(results_dir / f"{library.value}_load_db.txt") as f:
            time = timedelta(seconds=pytimeparse.parse(f.readline().strip().partition(": ")[2]))
            ram = f.readline().strip().partition(": ")[2]
            disk = f.readline().strip().partition(": ")[2]
        time = f"{time.total_seconds():.1f}"
        time_list.append(time)
        ram_list.append(ram)
        disk_list.append(disk)
    header = f"Load database"
    time_dict[header] = time_list
    ram_dict[header] = ram_list
    disk_dict[header] = disk_list
    return time_dict, ram_dict, disk_dict


def collect_query_data():
    time_dict = {}
    ram_dict = {}
    disk_dict = {}
    for what in What:
        time_list = []
        ram_list = []
        disk_list = []
        for library in Library:
            with open(results_dir / f"{library.value}_{what.value}_profile.txt") as f:
                time = timedelta(seconds=pytimeparse.parse(f.readline().strip().partition(": ")[2]))
                ram = f.readline().strip().partition(": ")[2]
                disk = f.readline().strip().partition(": ")[2]
            time_profile_path = results_dir / f"{library.value}_{what.value}_time_profile.txt"
            if time_profile_path.exists():
                with open(time_profile_path) as f:
                    time = timedelta(seconds=float(f.readline().strip()))
            time = f"{time.total_seconds():.1f}"
            time_list.append(time)
            ram_list.append(ram)
            disk_list.append(disk)
        header = f"Query {escape_underscore(what.value)}"
        time_dict[header] = time_list
        ram_dict[header] = ram_list
        disk_dict[header] = disk_list
    return time_dict, ram_dict, disk_dict


def generate_table(name, d):
    writer = MarkdownTableWriter()
    writer.table_name = name
    writer.from_dataframe(
        pd.DataFrame(d, index=[escape_underscore(library.value) for library in Library]),
        add_index_column=True
    )
    writer.dump(results_dir / f"{name}.md")


if __name__ == "__main__":
    time_dict, ram_dict, disk_dict = collect_load_db_data()
    generate_table("Load database time", time_dict)
    generate_table("Load database RAM", ram_dict)
    generate_table("Load database disk", disk_dict)

    time_dict, ram_dict, disk_dict = collect_query_data()
    generate_table("Query time", time_dict)
    generate_table("Query RAM", ram_dict)
    generate_table("Query disk", disk_dict)

