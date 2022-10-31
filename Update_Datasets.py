import os,json,urllib.request,config
from io import BytesIO
from zipfile import ZipFile

CONF = config.Config()


def Download_NaPTAN():
    URL = "https://naptan.api.dft.gov.uk/v1/access-nodes?dataFormat=csv"
    NaPTAN_Data = urllib.request.urlretrieve(URL,"NaPTAN Dataset Stops.csv")
    return "NaPTAN Dataset Stops.csv"

def Download_GTFS_Files():
    FLS=[]
    for FILE,URL in CONF.GTFS_FILES_TO_UPDATE.items():
        resp = urllib.request.urlopen(URL)
        GTFS_ZIP = ZipFile(BytesIO(resp.read()))
        GTFS_ZIP.extractall(path=f"Input/{FILE}/")
        FLS.append(f"Input/{FILE}/")
    return "\n".join(FLS)

print(Download_NaPTAN())
print(Download_GTFS_Files())