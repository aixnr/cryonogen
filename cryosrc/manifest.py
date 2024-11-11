import sqlite3
import pandas as pd

class Manifest:
    def __init__(self, conn: sqlite3.Connection):
        self.boxes = pd.read_sql("SELECT * FROM boxes", con=conn)
        self.vials = pd.read_sql("SELECT * FROM vials", con=conn)

    def return_box_index(self) -> dict:
        # For listing all boxes on the index page
        payload: dict = {
            "status": 200, "message": "OK",
            "data": self.boxes.to_dict(orient="records")
        }

        return payload
    
    def return_box(self, box_id: str) -> dict:
        # For displaying box infection on each box's page
        _box = self.boxes.query(f" BoxID == '{box_id}' ")
        payload: dict = {
            "status": 200, "message": "OK",
            "data": _box.to_dict(orient="records")
        }

        return payload
    
    def return_all_vials(self) -> dict:
        # For the search page
        payload: dict = {
            "status": 200, "message": "OK",
            "data": self.vials.to_dict(orient="records")
        }

        return payload
    
    def return_vials_box(self, box_id: str) -> dict:
        # For each box's page
        _vials = self.vials.query(f" BoxID == '{box_id}' ")

        payload: dict = {
            "status": 200, "message": "OK",
            "cellArray": _vials.to_dict(orient="records")
        }

        return payload
