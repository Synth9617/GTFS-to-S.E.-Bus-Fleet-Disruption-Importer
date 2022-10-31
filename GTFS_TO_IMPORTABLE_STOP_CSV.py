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
import csv,config, CoordConversion

CONF = config.Config()

GTFS_FILES = CONF.GTFS_FILES

STOPS = {}
STOPS_MISSING = []
with open("NaPTAN Dataset Stops.csv",'r') as f: # CSV File downloaded from Gov.UK site: https://www.data.gov.uk/dataset/ff93ffc1-6656-47d8-9155-85ea0b8f2251/national-public-transport-access-nodes-naptan
    NaPTAN = list(csv.DictReader(f))
    print(len(NaPTAN))
    for line in NaPTAN: # Cycles through the CSV and creates a dictionary of stops with the ATCO as the key.
        if [line["Latitude"],line["Longitude"]] == ["",""]:
            E = line['Easting']
            N = line['Northing']
            EN = CoordConversion.ENtoLL84(E,N)

            line["Longitude"] = EN[0]
            line["Latitude"] = EN[1]

        LINE_DATA = {
            "name":f"{line['LocalityName']}, {line['CommonName']} ({line['Indicator']})",
            "indicator":str(line['Indicator']),
            "locality":str(line['LocalityName']),
            "direction":str(line['Bearing']),
            "latitude":line['Latitude'],
            "longitude":line['Longitude'],
            "atco":line["ATCOCode"]
        }
        STOPS[str(line["ATCOCode"])]=LINE_DATA

print(len(STOPS))

STOPS_FOR_IMPORT = []
for FILE in GTFS_FILES: # Supports multiple GTFS datasets
    with open(f"Input/{FILE}/stops.txt",'r') as f:
        for line in csv.DictReader(f): # Cycles through GTFS dataset stops.txt file (as a csv) to filter the NaPTAN dataset using the GTFS one. 
            ATCO = str(line["stop_id"]).upper()
            if ATCO not in STOPS:
                STOPS_MISSING.append(line)
            else:
                STOPS_DATA = STOPS[ATCO]
                if STOPS_DATA not in STOPS_FOR_IMPORT:
                    if "" not in [STOPS_DATA['latitude'],STOPS_DATA['longitude']]: # Will not include stops which have no location data on the NaPTAN dataset
                        print(STOPS_DATA['name'])
                        STOPS_FOR_IMPORT.append(STOPS_DATA)

print(len(STOPS_MISSING)) # Returns amount of ATCOs from the GTFS file that were not in the NaPTAN dataset.

FN = [
    "name",
    "direction",
    "latitude",
    "longitude",
    "atco",
    "locality",
    "indicator"
    ]
with open("Output/GTFS_to_CSV_Stops_Importable.csv",'w',newline="") as f: # Saves the final list of stops to a CSV ready for import into the map
    writer = csv.DictWriter(f,fieldnames=FN)
    writer.writeheader()
    writer.writerows(STOPS_FOR_IMPORT)