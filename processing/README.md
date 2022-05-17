(under construction)

## Background

This script is designed to read data from the Retail Price Index with Details (RPID) spreadsheets published by the United Nations International Civil Service Commission (UN ICSC), and write those data into a more usable form. 

The original data (https://unicsc.org/Home/DataRPI) are spread across various spreadsheets, and the spreadsheets are macro-enabled and password-protected in such a way that retail price index data for a given time can only be displayed one country at a time.  Thus, although these data are public, they are hard to use for analyses over space and time.  

This script was originally developed and tested using RPID spreadsheets from 2004 through 2021. However, the script was also written with future data processing needs in mind.  As new RPID spreadsheets are released by the UN, librarians at Brown can download them into a specific folder, run the script, and immediately have updated data.
 
## Notes on Project File Structure

This script is not a standalone piece of code.  The designated folder for RPID spreadsheets (original_data -> rpid) is not included in this remote copy of the repository.  This means that making a clone of this repository and trying to run the script will not work unless a Every time the script processes a spreadsheet, that spreadsheet's file name is appended to already_done_file_list.csv, which lists the names of spreadsheets that have already been processed. By keeping track of these spreadsheets, we can download future UN ICSC spreadsheets into a designated folder and then just run the script, and it will produce updated data based on the new spreadsheets without re-processing all of the old ones. Having this file also means that specific old spreadsheets can be re-processed by deleting those file names from the "already done" file, saving it, and then running the script again.

This script is therefore not a "standalone" piece of code.  In addition to reading the aforementioned "already done files" csv, the script also reads and maintains local files containing supplementary information like ISO codes and index categories, since this was preferable to having this information hard-coded into the script.  When supplementary information is not sufficient for a particular case, the script will ask for the user to type in missing information while the script is running, and those supplemental files will be updated accordingly.

In addition to relying on files within its directory or sub-folders, the script also reads in spreadsheets from a separate file location within the GIS and Data Services shared drive, which the script accesses by navigating up to its grandparent directory and then down a different branch of the folder tree.  This was an intentional choice informed by a specific set of file management needs for Brown.  Because of this, the script cannot be readily "packaged up" in a zipped folder and run elsewhere without first editing the file path for input spreadsheets (i.e. the variable named SHEETS_PATH) in this script to conform to a different directory structure.

## Notes on Libraries, Data Structures, and Script Logic

This script uses the xlwings library to read in spreadsheet data due to its specific functionalities compared to other Python libraries for Excel.  In particular, xlwings is able to interact with files stored under both the old and new Excel formats, and it can interact with both cell values and formulae.
 
Lists are the primary data structure used within the script to store and append data iteratively, but some data are temporarily converted to pandas dataframes for column operations. ISO code and category code lookups are handled with dictionaries (hashtables).

Supplementary information like country ISO codes are updated dynamically by having the user type inputs into the Python console while the script is running for any country names which don't exactly match a country name currently in the supplementary information.  This functionality helps handle the fact that many country names have either changed officially or been referred to differently by the UN within this almost 20 year old dataset.

To walk through the script code in the order of execution at a high level, navigate to the READY TO RUMBLE section of the file and start reading the inline comments from there.