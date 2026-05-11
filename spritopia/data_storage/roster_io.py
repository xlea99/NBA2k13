import time
from spritopia.common.logger import log
from spritopia.common.paths import paths
from spritopia.interface.red_mc import RedMC
from spritopia.data_storage.data_storage import d

# This helper file combines data_storage and redmc methods to facilitate importing
# and exporting all data between the program and RedMC.


# RedMC -> PROGRAM
# This method imports all CSVs from the given %rosterName%.ROS file into the local program CSV
# data folder and dataStorageObject.
def importRosterData(rosterName,dataStorageObject):
    # Pre-create the destination dir so RedMC's save dialog doesn't have to.
    # Some RedMC builds silently fail when typing a path to a non-existent
    # folder rather than creating it.
    target_dir = paths["rosterCSVs"] / rosterName
    target_dir.mkdir(parents=True, exist_ok=True)

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
