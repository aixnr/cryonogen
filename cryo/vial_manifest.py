"""vial_manifest.py
For returning dictionary of Vial Information
"""
# Import modules
import pandas as pd
from .env import constants as cts


class Vial:
    def __init__(self):
        # List all sheets and read them
        _sheet_list = pd.ExcelFile(cts["sheet_manifest_vial"]).sheet_names
        _df = pd.concat([pd.read_excel(cts["sheet_manifest_vial"], sheet_name=sheet) for sheet in _sheet_list])

        # If shortName does not exist, filter it out, '~' means 'is not'
        _df = _df[~_df["shortName"].isnull()]

        # Replace np.NaN with empty string
        _df = _df.fillna("")

        # Combine reagentConc and initialVolume as reagentSize
        _df["reagentSize"] = _df.apply(lambda x: "{} ({})".format(x["reagentConc"], x["initialVolume"]) if len(x["initialVolume"]) > 0 else x["reagentConc"], axis=1)

        # If vialCount and vialSequence are present, combine into vialOrder
        # commented on 2024-JUL-04
        # _df["vialOrder"] = _df.apply(lambda x: "#{:.0f}/{:.0f}".format(x["vialSequence"], x["vialCount"]) if x["vialCount"] > 1 else "1 vial", axis=1)

        # Finally, combine reagentSize and vialOrder as vialMeta
        # _df["vialMeta"] = _df.apply(lambda x: "{}, {}".format(x["reagentSize"], x["vialOrder"]), axis=1)
        # modified on 2024-JUL-04
        _df["vialMeta"] = _df.apply(lambda x: "{}".format(x["reagentSize"]), axis=1)

        # Drop columns and save to self
        # _drop_list = ["reagentConc", "initialVolume", "vialSequence", "vialCount", "reagentSize", "vialOrder"]
        _drop_list = ["reagentConc", "initialVolume", "reagentSize"]
        self._df = _df.drop(columns=_drop_list)

    def return_all_vials(self):
        payload = {
            "status": 200, "message": "OK",
            "data": self._df.to_dict(orient="records")
        }

        return payload

    def return_vials_box(self, box_id: str):
        """
        TODO:
          - HANDLE RETURN WHEN BoxID IS NOT PRESENT
        """
        # Retrieve data for the box and remove absentStatus column
        _df_vial_box = self._df.query(f" BoxID == '{box_id}' & absentStatus != 1 ").drop(columns=["absentStatus"])

        payload = {
            "status": "200", "message": "OK",
            "cellArray": _df_vial_box.to_dict(orient="records")
        }

        return payload

    def return_box_vial_status(self, box_id: str):
        """For box_manifest.return_box_index to use for providing the
          - remaining slots
          - last item add

        Return as a dictionary with BoxID as the key and value is dictionary of key:value pairs.
        """
        # Subset data
        _box_df = self._df.query(f" BoxID == '{box_id}' and absentStatus != 1 ")

        def slotFilled():
            # slotFilled == len(), i.e., length of rows
            return len(_box_df)

        def recentlyAdded():
            # Change dateDeposited from string to integer, then get the max value
            _box_df["dateDepositedInt"] = _box_df["dateDeposited"].apply(lambda x: int(x.replace("-", "")))
            _maxDateDepositedInt = max(_box_df["dateDepositedInt"])

            # Change back to string with month int to str (3-letter code) for clarity
            def month_str(x):
                m = str(_maxDateDepositedInt)[4:6]
                month_str_code = {"01": "JAN", "02": "FEB", "03": "MAR", "04": "APR", "05": "MAY", "06": "JUN",
                                  "07": "JUL", "08": "AUG", "09": "SEP", "10": "OCT", "11": "NOV", "12": "DEC"}
                return month_str_code[m]

            _maxDateDepositStr = "{}/{}/{}".format(str(_maxDateDepositedInt)[0:4],
                                                   month_str(_maxDateDepositedInt),
                                                   str(_maxDateDepositedInt)[6:8])

            _lastItem = _box_df.query(f" dateDepositedInt == {_maxDateDepositedInt} ")["shortName"].to_list().pop()

            # Return the shortName of the last item and (clarified) date string
            return _lastItem, _maxDateDepositStr

        # Run sub-functions and return the data
        boxCurrentVialStatus = {"slotFilled": slotFilled(), "recentlyAdded": recentlyAdded()}
        return boxCurrentVialStatus
