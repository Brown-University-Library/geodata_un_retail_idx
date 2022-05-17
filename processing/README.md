## Notes on script functionality

Retail Price Indices with Details (RPID) spreadsheets downloaded from the [UN ICSC website](https://unicsc.org/Home/DataRPI) are macro-enabled and password protected in such a way that they only display cost-of-living data for one country at a time. Furthermore, each year-month of data is in a separate spreadsheet.  As a result, these spreadsheets are cumbersome to use for comparing data from different countries and/or over time.  

This script starts with a designated folder containing a collection of RPID spreadsheets and iterates through each country within each spreadsheet in that folder, writing the data to .csv files that display the data from multiple countries and from multiple time periods in a single place.  

While the script is running, prompts for user input may be printed in the Python console or terminal.  In particular, one of the things the script does is add an identifying ISO code for each country name it reads in from the RPID spreadsheets, and country names can change from one year to the next, so the user may be asked to type in the three-character ISO code for a version of a country name that isn't present in the script's supplementary information files.  This will only occur once for each occurence of a new version of a country name - the script will save the user input in its supplementary information files and use it for any future occurrences of that version of a country name.

Every time the script processes a spreadsheet, that spreadsheet's file name is appended to ```already_done_file_list.csv```.  Then, when new RPID data are released by the UN, they can be downloaded into a designated folder (original_data -> rpid), and when the script is run again, it only processes the new spreadsheets instead of re-doing all the ones that had already been processed on previous script runs.

Cloning this repository somewhere and trying to run the script without any extra modifications will fail, because the designated folder containing the original RPID spreadsheets is not included in the remote version of this repository.
