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
#   Arriva, First, and Stagecoach do not use GTFS, but do use British-standard TransXChange format. 
#   We do know of a tool for converting TransXChange to GTFS, but it only runs on Linux and uses NPM (Node.JS)
#   It is NOT developed by us, but we do use it and do approve of it: https://www.npmjs.com/package/transxchange2gtfs
#
#########################

##### DO NOT EDIT ANYTHING BELOW THIS!!!! #####
import csv,json,config

CONF = config.Config()

GTFS_FILES = CONF.GTFS_FILES
OPERATOR_ALIAS = CONF.OPERATOR_ALIAS

STOPS = []
ROUTES = {}
STOPS_ROUTES = {}
TRIP_ROUTE = {}

for FILE in GTFS_FILES:
    with open(f"Input/{FILE}/trips.txt",'r') as trip_file:
        for trip_line in csv.DictReader(trip_file):
            TRIP_ROUTE[trip_line['trip_id']] = trip_line['route_id']

    with open(f"Input/{FILE}/stops.txt",'r') as stop_file:
        for line in csv.DictReader(stop_file):
            STOPS.append(line)

    with open(f"Input/{FILE}/routes.txt",'r') as route_file:
        for line in csv.DictReader(route_file):
            ROUTES[line['route_id']] = line

    with open(f"Input/{FILE}/stop_times.txt",'r') as timing_file:
        for line in csv.DictReader(timing_file):
            route_code = TRIP_ROUTE[line['trip_id']]
            ROUTE = ROUTES[route_code]

            ATCO = line["stop_id"]
            GTFS_NOC = ROUTE['agency_id']
            if GTFS_NOC in OPERATOR_ALIAS:
                GTFS_NOC = OPERATOR_ALIAS[GTFS_NOC]
            ROUTE_DATA = {
                    "line_name":ROUTE['route_short_name'],
                    "operator":GTFS_NOC
                }

            if ATCO not in STOPS_ROUTES:
                STOPS_ROUTES[line['stop_id']] = [ROUTE_DATA]
            else:
                lst = list(STOPS_ROUTES[ATCO])
                if ROUTE_DATA not in lst:
                    lst.append(ROUTE_DATA)
                    STOPS_ROUTES[ATCO]=lst

print(len(STOPS_ROUTES))
with open("Output/GTFS_to_CSV_Stops_Routes_M2M_Importable.json",'w') as json_file:
    json.dump(STOPS_ROUTES,json_file,indent=4)
