import csv
import json
import re
import datetime
from time import strptime

def get(config):

    # Read in the CSV data:
    with open(config["csv_source"], "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Create starting data, including root UON info from config:
    py_data = {
        "areas": config["uon_data"],
        "depts": {},
        "persons": {},
        "excluded": []
    }

    done = 0

    # Take the data line by line:
    for d in data:

        # Flag to determine whether or not to include a staff member:
        process_staff = True

        # Filter out staff based on alphanumeric ResID values (e.g. jsmith):
        staff_pattern=re.compile("\D")
        if staff_pattern.search(d["ResID"]):
            # Pop them into the excluded list:
            py_data["excluded"].append (
                {
                    "resid": d["ResID"],
                    "studentid": d["Student_ID"],
                    "name": d["FORENAMES"] + " " + d["SURNAME"]
                }
            )
            # Bail out:
            continue
        
        if not d["START_DATE"]:
           print(f"No start date for {d['ResID']}")
           continue

        # We've probably got a student, so grab what we need:
        # Flip the date:
        startdate_obj = datetime.datetime.strptime(d["START_DATE"], "%d/%m/%Y")
        startdate = startdate_obj.strftime("%Y-%m-%d")
        py_data["persons"][d["ResID"]] = {
            "title": d["TITLE"],
            "firstname": d["FORENAMES"],
            "lastname": d["SURNAME"],
            "email": d["EMAIL"],
            "description": d["Course Desc"],
            "startdate": startdate
        }
        
        
    return py_data