#########################
#
# Author: Katherine Toms (Synth9617)
# Websites: 
#   - https://busstopdistruptionmap.tomscatbilly9617.com/
#   - https://sebusfleet.tomscatbilly9617.com/
#   - https://accessible-buses.co.uk/
#
#   This script is for use with our import tool. You can adapt it to work with your own projects & needs. 
#   You can download GTFS files from most operators that use the Passenger websites and apps,
#   A few examples of operators include all of Go-Ahead Group UK's Bus Operations, Reading Buses, and many independant operators.
#
#   The datasets found on the Gov.UK Open Data system do not use GTFS, but instead use the British-standard TransXChange format. 
#   We do know of a tool for converting TransXChange to GTFS, but it only runs on Linux and uses NPM (Node.JS)
#   It is NOT developed by us, but we do use it and do approve of it: https://www.npmjs.com/package/transxchange2gtfs
#
#########################

##### DO NOT EDIT ANYTHING BELOW THIS!!!! #####
import csv,config

CONF = config.Config()

GTFS_FILES = CONF.GTFS_FILES
OPERATOR_ALIAS = CONF.OPERATOR_ALIAS

ROUTES = []
for FILE in GTFS_FILES: # Supports multiple GTFS datasets
    with open(f"Input/{FILE}/routes.txt",'r') as f:
        for line in csv.DictReader(f):
            GTFS_NOC = line['agency_id']
            if GTFS_NOC in OPERATOR_ALIAS:
                GTFS_NOC = OPERATOR_ALIAS[GTFS_NOC]

            StartPoint = ""
            EndPoint = ""
            if " - " in line['route_desc']:
                desc = str(line["route_desc"]).split(" - ")
                StartPoint = desc[0]
                EndPoint = desc[len(desc)-1]

            ROUTES.append({
                "RouteName":line['route_short_name'],
                "RouteNumber":line['route_short_name'],
                "Operator":GTFS_NOC,
                "RouteColor":line['route_color'],
                "LabelColour":line["route_text_color"],
                "StartPoint":StartPoint,
                "EndPoint":EndPoint
            })
        
FN = ["RouteName","RouteNumber","Operator","RouteColor","LabelColour","StartPoint","EndPoint"]
with open("Output/GTFS_to_CSV_Routes_Importable.csv",'w',newline="") as f: # Saves the final list of routes to a CSV ready for import into the map
    writer = csv.DictWriter(f,fieldnames=FN)
    writer.writeheader()
    writer.writerows(ROUTES)