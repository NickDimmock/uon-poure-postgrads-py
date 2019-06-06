import csv
import json
import re
import datetime
from time import strptime

def get(config):

    # Set headers for CSV data:
    csv_fieldnames=[
        'rel_value',
        'student_id',
        'res_id',
        'title',
        'forenames',
        'surname',
        'email',
        'start_date',
        'division_code',
        'division_name',
        'course_code',
        'course_desc',
        'ft_pt'
    ]
    # Read in the CSV data:
    with open(config["csv_source"], "r") as f:
        reader = csv.DictReader(f, fieldnames = csv_fieldnames)
        data = list(reader)

    # Create starting data, including root UON info from config:
    py_data = {
        "areas": config["uon_data"],
        "depts": {},
        "persons": {},
        "excluded": []
    }

    # A list of our various complaints:
    problems = []

    # Take the data line by line:
    for d in data:

        # Filter out staff based on alphanumeric res_id values (e.g. jsmith):
        # Strip the res_id, as it sometimes has a leading space...
        staff_pattern=re.compile("\D")
        if staff_pattern.search(d["res_id"].strip()):
            # Pop them into the excluded list:
            py_data["excluded"].append (
                {
                    "res_id": d["res_id"],
                    "studentid": d["student_id"],
                    "name": d["forenames"] + " " + d["surname"]
                }
            )
            problems.append({
                "res_id": d['res_id'],
                "studentid": d["student_id"],
                "forenames": d["forenames"],
                "surname": d["surname"],
                "email": d["email"],
                "problem": "res_id doesn't match ARMS pattern - may be staff"
            })
            # Bail out:
            continue
        
        if not d["start_date"]:
           problems.append({
                "res_id": d['res_id'],
                "studentid": d["student_id"],
                "forenames": d["forenames"],
                "surname": d["surname"],
                "email": d["email"],
                "problem": "No start date provided"
           })
           continue

        # We've probably got a student, so grab what we need:
        # Flip the date:
        startdate_obj = datetime.datetime.strptime(d["start_date"], "%d/%m/%Y")
        startdate = startdate_obj.strftime("%Y-%m-%d")
        py_data["persons"][d["res_id"].strip()] = {
            "title": d["title"],
            "first_name": d["forenames"],
            "surname": d["surname"],
            "email": d["email"],
            "description": d["course_desc"],
            "startdate": startdate
        }
        
    with open(config["error_file"], "w", encoding="utf-8") as f:
        f.write(json.dumps(problems, indent=4))
    return py_data