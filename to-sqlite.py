import pandas as pd
import sqlite3
from typing import Dict
from argparse import ArgumentParser


def collect_vials(xlsx: pd.ExcelFile) -> pd.DataFrame:
    _vials: Dict[str, pd.DataFrame] = {}

    for sheet in xlsx.sheet_names:
        _vials[sheet] = (
            pd.read_excel(xlsx, sheet)
            .drop(columns=["absentStatus"])
            .dropna(subset=["shortName"])
            .fillna("")
            )

    _df: pd.DataFrame = pd.concat(_vials.values()).reset_index(drop=True)
    _df["reagentSize"] = _df.apply(lambda x: "{} ({})".format(x["reagentConc"], x["initialVolume"]) if len(x["initialVolume"]) > 0 else x["reagentConc"], axis=1)
    _df["vialMeta"] = _df.apply(lambda x: "{}".format(x["reagentSize"]), axis=1)
    _drop_list = ["reagentConc", "initialVolume", "reagentSize"]
    return _df.drop(columns=_drop_list)


def collect_boxes(xlsx: pd.ExcelFile) -> pd.DataFrame:
    _df = pd.read_excel(xlsx)
    _df = _df.fillna("")
    _df["storageLocation"] = _df.apply(lambda x: "{}, {} ({})".format(x["parentLocation"], x["storageIdentifier"], x["storageTemp"]), axis=1)
    _df["storageLocation"] = _df.apply(lambda x: "{}, at {}".format(x["storageLocation"], x["specificLocation"]) if len(x["specificLocation"]) > 0 else x["storageLocation"], axis=1)
    _drop_list = ["parentLocation", "storageIdentifier", "storageTemp", "specificLocation"]
    return _df.drop(columns=_drop_list)


def box_meta(boxes: pd.DataFrame, vials: pd.DataFrame) -> pd.DataFrame:
    _current_capacity: int = []
    for _box in boxes["BoxID"]:
        _vial_box = vials.query(f" BoxID == '{_box}' ")
        _vial_box_rows = len(_vial_box)
        _current_capacity.append(_vial_box_rows)
    
    _boxes_df = boxes.copy()
    _boxes_df["currentCapacity"] = _current_capacity
    _boxes_df["currentCapacity"] = _boxes_df.apply(lambda x: "{}/{}, {:.0f}%".format(x["currentCapacity"], x["boxCapacity"], 100 * (x["currentCapacity"] / x["boxCapacity"])), axis=1)

    _box_type: Dict[int, str] = {81: "9-9", 64: "8-8", 10: "10-10"}
    _boxes_df["boxType"] = _boxes_df["boxCapacity"].apply(lambda x: _box_type[x])
    
    return _boxes_df


def to_sqlite(path_box: str, path_vial: str) -> None:
    vials = pd.ExcelFile(path_vial)
    boxes = pd.ExcelFile(path_box)

    conn = sqlite3.connect("cryonogen.db")

    collect_vials(vials).to_sql("vials", con=conn, if_exists="replace", index=False)
    box_meta(boxes=collect_boxes(boxes), vials=collect_vials(vials)).to_sql("boxes", con=conn, if_exists="replace", index=False)

    conn.close()


if __name__ == "__main__":
    parser = ArgumentParser(description="BoxManifest and VialManifest SQLite Prep Script")
    subparsers = parser.add_subparsers(dest="command")

    process_parser = subparsers.add_parser("process")
    process_parser.add_argument("--box", type=str, help="Path to the BoxManifest spreadsheet.")
    process_parser.add_argument("--vial", type=str, help="Path to the VialManifest spreadsheet.")

    args = parser.parse_args()

    if args.command == "process":
        if args.box and args.vial:
            to_sqlite(path_box=args.box, path_vial=args.vial)
            print("Completed persisting data to 'cryonogen.db' SQLite database")
            print("Exiting...")
            exit(0)
        else:
            print("Error: Both --box and --vial arguments are required.")
            parser.print_help()
            exit(1)
    else:
        parser.print_help()
        exit(1)
