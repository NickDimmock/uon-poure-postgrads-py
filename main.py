#import create_orgs
import create_persons
import create_users
import get_data
import json

with open ('config.json', 'r') as f:
    config = json.load(f)

# Parse the CSV data:
data = get_data.get(config=config)

'''
# Person data structure:
{
    "id": "12345678",
    "firstname": "John",
    "lastname": "Doe",
    "startdate": "31/01/2018"
}  
'''

#print(len(data["persons"]))
#print(len(data["excluded"]))
#print(data["persons"])
#print(data["excluded"])

# Combine uni, faculty and dept data to send to org creation function:
#org_data = {**data["areas"], **data["depts"]}

# Create org data:
#create_orgs.create(config=config, data=org_data)

# Create person data:
create_persons.create(config=config, data=data["persons"])

# Create user data:
create_users.create(config=config, data=data["persons"])
