import json
class Config:
    def __init__(self) -> None:
        with open("config.json",'r') as f:
            data = json.load(f)
            self.GTFS_FILES_TO_UPDATE = dict(data['GTFS_FILES_TO_UPDATE'])
            self.GTFS_FILES = list(data['GTFS_FILES'])
            self.OPERATOR_ALIAS = dict(data['OPERATOR_ALIAS'])