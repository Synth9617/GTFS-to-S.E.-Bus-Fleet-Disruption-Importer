#!/bin/sh

if [ -d "Input" ]; then
	mkdir "Input"
fi
if [ -d "Output" ]; then
	mkdir "Output"
fi

python3 Update_Datasets.py
python3 GTFS_to_CSV_ROUTES.py
python3 GTFS_TO_IMPORTABLE_STOP_CSV.py
python3 GTFS_TO_JSON_STOP_ROUTES.py