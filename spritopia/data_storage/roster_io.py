import time
from spritopia.common.logger import log
from spritopia.interface.red_mc import RedMC


# This helper file combines data_storage and redmc methods to facilitate importing
# and exporting all data between the program and RedMC.


# RedMC -> PROGRAM
# This method imports all CSVs from the given %rosterName%.ROS file into the local program CSV
# data folder and dataStorageObject.
def importRosterData(rosterName,dataStorageObject):
    r = RedMC()
    r.openRedMC()
    r.loadRoster(rosterName)
    r.exportCSVs(rosterName)
    r.closeRedMC()
    time.sleep(2)
    dataStorageObject.csv_ImportCSVs(rosterName)

    log.info(f"Imported roster data for roster '{rosterName}'")
    return r.testIfRedMCClosed()

# PROGRAM -> RedMC
# exportRosterData then exports internal program CSV data into actual CSV files, then exports
# those 4 CSV files into the actual %rosterName%.ROS file using RedMC.
def exportRosterData(rosterName,dataStorageObject):
    dataStorageObject.csv_ExportCSVs(rosterName)
    r = RedMC()
    r.openRedMC()
    r.loadRoster(rosterName)
    r.importCSVs(rosterName)
    r.saveRoster()
    r.closeRedMC()

    log.info(f"Exported roster data for roster '{rosterName}'")
    return r.testIfRedMCClosed()