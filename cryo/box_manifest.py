"""box_manifest.py
For returning dictionary of Box Information

"""
# Import modules
import pandas as pd
from .env import constants as cts
from .vial_manifest import Vial


class Box:
    def __init__(self):
        # Read data
        _df = pd.read_excel(cts["sheet_manifest_box"])

        # Replace np.NaN with empty string
        _df = _df.fillna("")

        # Combine parentLocation, storageIdentifier, and storageTemp into storageLocation
        _df["storageLocation"] = _df.apply(lambda x: "{}, {} ({})".format(x["parentLocation"], x["storageIdentifier"], x["storageTemp"]), axis=1)

        # If _df["specificLocation"] is not empty, add it to the _df["storageLocation"]
        _df["storageLocation"] = _df.apply(lambda x: "{}, at {}".format(x["storageLocation"], x["specificLocation"]) if len(x["specificLocation"]) > 0 else x["storageLocation"], axis=1)

        # Drop columns and save to self
        _drop_list = ["parentLocation", "storageIdentifier", "storageTemp", "specificLocation"]
        self._df = _df.drop(columns=_drop_list)

    def return_all_boxes(self):
        payload = {
            "status": 200, "message": "OK",
            "data": self._df.to_dict(orient="records")
        }

        return payload

    def return_box(self, box_id: str):
        """
        TODO:
          - HANDLE RETURN WHEN BoxID is not present (i.e. retrieve list of boxes registered and check against them)
        """
        _df_box = self._df.query(f" BoxID == '{box_id}' ")

        payload = {
            "status": 200, "message": "OK",
            "data": _df_box.to_dict(orient="records")
        }

        return payload

    def return_box_index(self):
        """Return additional information for the homepage (boxCapacity)
        """
        _vial = Vial()

        def filledStatus(x):
            boxVialStatus = _vial.return_box_vial_status(box_id=x["BoxID"])

            _slotFilled = boxVialStatus["slotFilled"]
            _boxCapacity = x["boxCapacity"]
            _slotFilledPercent = f"{(_slotFilled / _boxCapacity) * 100:.0f}"

            return "{}/{} ({}%)".format(_slotFilled, _boxCapacity, _slotFilledPercent)

        def recentlyAdded(x):
            boxVialStatus = _vial.return_box_vial_status(box_id=x["BoxID"])
            return boxVialStatus["recentlyAdded"]

        # Dictionary for box type (for linking href on the frontend)
        _box_type_dict = {81: "9-9", 64: "8-8", 100: "10-10"}

        _df = self._df.copy()
        _df["boxStatus"] = _df.apply(lambda x: filledStatus(x), axis=1)
        _df["recentlyAdded"] = _df.apply(lambda x: recentlyAdded(x), axis=1)
        _df["boxType"] = _df["boxCapacity"].apply(lambda x: _box_type_dict[x])

        payload = {
            "status": 200, "message": "OK",
            "data": _df.to_dict(orient="records")
        }

        return payload
