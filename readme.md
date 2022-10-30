
# GTFS to S.E. Bus Fleet Disrtuption Importer

These scripts are for use with our import tool. You can adapt it to work with your own projects & needs.

You can download GTFS files from most operators that use the [Passenger](https://passenger.tech/) websites and apps
A few examples of operators include all of [Go-Ahead Group UK's Bus Operations](https://www.go-ahead.com/who-we-are/uk-bus), [Reading Buses](https://www.reading-buses.co.uk/), and many independant operators.

## Using The TransXChange format instead of GTFS
The datasets found on the Gov.UK Open Data system do not use GTFS, but instead use the British-standard TransXChange format. 
We do know of a tool for converting TransXChange to GTFS, but it only runs on Linux and uses NPM (Node.JS)
It is NOT developed by us, but we do use it and do approve of it: https://www.npmjs.com/package/transxchange2gtfs


# Setting the config files
## GTFS_FILES
This should be a list of the paths to the folder of GTFS files. 
The folder listed in the GTFS_FILES listing MUST be a valid GTFS dataset with the following files.
| filename | purpose |
|----------|---------|
|agency.txt | Lists the operators included in the dataset|
|calendar.txt | Defines the days of the week a trip runs.|
|calendar_dates.txt | Defines any Bank Holidays for a trip|
|routes.txt| Provides some data for the routes and who operates them|
|shapes.txt| Used to draw the route on a map|
|stop_times.txt| The timetable data. (When a trip is scheduled to serve a stop|
|stops.txt| Provides the data for a stop, such as it's name and location|
|trips.txt| Indicates which what route the trip is, it's direction and running card 

### An Example is saved below!
``` json
"GTFS_FILES":[
        "carouselbuses_1662132222"
    ]
```

## OPERATOR_ALIAS
For use with CSLB & OXBC GTFS Datasets, which have 'Arriva Beds & Bucks' listed as 'Arriva The Shires'. Add more as required.

For use with operators who use multiple National Operator Code (which can be found here: [Traveline Open-data - Browse](https://www.travelinedata.org.uk/traveline-open-data/transport-operations/browse/)).


The Alternative NOC is the provided NOC, whereas the Canoncial NOC is the one that will be use instead of the alternative NOC.
| Alternative NOC | Canoncial NOC |
|-|-|
|ASES|ARBB|
|REDL|RLNE|

### An Example is saved below!
``` json
"OPERATOR_ALIAS":{
    "ASES":"ARBB",
    "REDL":"RLNE"
}

```

# Running The Scripts
This section will be split into the 3 importers used on our admin portal.
## Bus Stop Import Tool
### Python File: `GTFS_TO_IMPORTABLE_STOP_CSV`
### Output File: `GTFS_to_CSV_Stops_Importable.csv`
This script uses the GTFS dataset in conjuction with the [DfT's NaPTAN dataset](https://www.data.gov.uk/dataset/ff93ffc1-6656-47d8-9155-85ea0b8f2251/national-public-transport-access-nodes-naptan) to create a CSV file of the stops used, with the name of `GTFS_to_CSV_Stops_Importable.csv` in the Output folder.

If the script errors out due to a stop not being listed in the NaPTAN file, please update the `NaPTAN Dataset Stops.csv` file with the new data from the DfT's site above.

An example of the CSV is as follows:
|name|direction|latitude|longitude|atco|locatity|indicator|
|-|-|-|-|-|-|-|
High Wycombe, Oxford Street (Stop J)|E|51.630941|-0.753404|040000003058|High Wycombe|Stop J|

## Bus Route Import Tool
### Python File: `GTFS_to_CSV_ROUTES.py`
### Output File: `GTFS_to_CSV_Routes_Importable.csv`
This script converts the route data from the GTFS datasets into a CSV file, with the name of `GTFS_to_CSV_Routes_Importable.csv` in the Output folder, for the backend to understand.

An example of the CSV is as follows:

|RouteName|RouteNumber|Operator|RouteColor|LabelColour|
|-|-|-|-|-|
|Chiltern Hundreds 102|102|CSLB|#EC7C07|#FFFFFF|

## Bus Route with Stops Import Tool
### Python File: `GTFS_TO_JSON_STOP_ROUTES.py`
### Output File: `GTFS_to_CSV_Stops_Routes_M2M_Importable.json`

This script creates a JSON dictionary of bus stops with any routes that serve them.

An example of the JSON file is as follows:
``` json
{
    "040000003058": [
        {
            "line_name": "1",
            "operator": "CSLB"
        },
        {
            "line_name": "1A",
            "operator": "CSLB"
        },
        {
            "line_name": "1B",
            "operator": "CSLB"
        }
    ]
}
    
```