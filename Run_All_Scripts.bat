if not exist "Input" mkdir "Input"
if not exist "Output" mkdir "Output"

python Update_Datasets.py
timeout 15 > NUL
python GTFS_to_CSV_ROUTES.py
python GTFS_TO_IMPORTABLE_STOP_CSV.py
python GTFS_TO_JSON_STOP_ROUTES.py
pause