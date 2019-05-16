import xml.etree.ElementTree as ET
import xml.dom.minidom

def create(config, data):
    
    users = ET.Element("users")

    for ns, uri in config["users_namespaces"].items():
        users.set(ns, uri)

    for id, obj in data.items():

        user = ET.SubElement(users, "user")
        user.set("id", f"user-{id}")

        # We need a padded 8-digit version of our ID for the username value:
        padded_id = id.rjust(8, "0")

        username = ET.SubElement(user, "userName")
        username.text = padded_id

        email = ET.SubElement(user, "email")
        email.text = obj["email"]

        name = ET.SubElement(user, "name")
        name_first = ET.SubElement(name, "v3:firstname")
        name_first.text = obj["first_name"]
        name_last = ET.SubElement(name, "v3:lastname")
        name_last.text = obj["surname"]
    
    # Create XML string, then use minidom to generate a readable version
    xml_string = ET.tostring(users, encoding="unicode")
    new_xml = xml.dom.minidom.parseString(xml_string)
    
    with open(config["users_xml"], "w", encoding="utf-8") as f:
        f.write(new_xml.toprettyxml())
    