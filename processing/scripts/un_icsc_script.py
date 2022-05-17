# Ethan McIntosh - Brown University - March 1, 2022

from datetime import datetime
import os
import pandas as pd
import xlwings as xw
import csv
import sys

# *************** CONSTANTS & GLOBAL VARIABLES *****************

# file paths to local supplementary files and to the input spreadsheets folder
ISO_TO_COUNTRY_FILE = 'iso_alpha3_to_country.csv'
COUNTRY_TO_ISO_FILE = 'country_to_iso_alpha3.csv'
CAT_CODE_FILE = 'category_codes.csv'
ALREADY_DONE_FILE = 'already_done_file_list.csv'
MEGA_FILE = "output_csvs/aggregate_csvs/all_un_icsc_rpid.csv"
PIVOTED_FILE = "output_csvs/aggregate_csvs/all_un_icsc_rpid_pivoted.csv"
EXTENT_FILE = "output_csvs/aggregate_csvs/data_extent.csv"
grandparent = os.path.dirname(os.path.dirname(os.getcwd())).replace("\\", "/")
SHEETS_PATH = grandparent + '/original_data/rpid'

# relevant cell ranges for UN ICSC RPID spreadsheets
PLACE_NAMES_START_CELL = 'B4'  # top of the list of all place names
PLACE_NAME_WRITE_CELL = 'AF2'  # name of the cell where place names are pasted
DATA_DATE_CELLS = ['E8', 'F6']  # possible cell locations of dataset date
DATA_READ_RANGE = 'AH2:AK17'  # range with weights, indices, and group names

# initialize global variables
prev_country = ""
iso_dict, reverse_iso_dict, cat_dict = ({},) * 3
cat_list, aggregate_list = ([],) * 2
extent = pd.DataFrame()

# specifies the order in which we want output columns to be displayed
column_names = ["unique_id", "yr_month", "iso_a3", "cmn_cntry", "un_cntry",
                "city", "cat_code", "group", "weight", "index"]
abbrev_dict = {'weight': 'wgt', 'index': 'idx'}  # pivoted file abbreviations
excel_app = xw.App(visible=False)  # virtual Excel instance


# *************** FUNCTIONS *****************

# Converts any indices in a given dataframe into columns.
def indices_to_columns(df):
    indices = df.index.names
    for i in reversed(indices):  # reversing the indices preserves column order
        df.reset_index(inplace=True, level=i)


# Reads in supplemental information from local files about ISO codes, category
# codes, and the current extent of the already processed data.
def initialize_dictionaries():
    global iso_dict, reverse_iso_dict, cat_dict, cat_list, aggregate_list, extent

    # dictionary with UN country names as keys and ISO codes as values
    iso_dict = pd.read_csv(COUNTRY_TO_ISO_FILE) \
        .set_index('country').to_dict()['iso_alpha3']

    # dictionary with ISO codes as keys and common country names as values
    reverse_iso_dict = pd.read_csv(ISO_TO_COUNTRY_FILE) \
        .set_index('iso_alpha3').to_dict()['name_common']

    # dictionary with category names as keys and cat codes as values
    cat_dict = pd.read_csv(CAT_CODE_FILE) \
        .set_index('group').to_dict()['cat_code']

    # list of categories, in the original order. Used for sorting purposes
    cat_list = pd.read_csv(CAT_CODE_FILE)['cat_code'].to_list()

    # read in the data_extent file as a dataframe
    extent = pd.read_csv(EXTENT_FILE, index_col='yr_month')

    # read in the mega-csv as a list of lists
    with open(MEGA_FILE, newline='', encoding='utf-8-sig') as fx:
        readerx = csv.reader(fx)
        aggregate_list = list(readerx)


# Processes the raw data that a given spreadsheet populates for each duty
# station place name, generating all of the columns that will be in the output,
# while performing checks and producing warning messages and/or input dialogs
# to handle unexpected values.
def arrange_data(input_list, place_name, data_date):
    global prev_country

    # these one-off checks were added to handle scenarios where the place
    # name was missing the " >> " and the city normally present
    if place_name == 'Dominican Republic':
        country = place_name
        city = 'Santo Domingo'
    elif place_name == 'New Caledonia':
        country = place_name
        city = 'NouMea'
    else:
        country = place_name.split('>>')[0].strip()
        city = place_name.split('>>')[1].strip()

    if country == prev_country:
        print("Warning: multiple records found in "
              + data_date + " for country + " + country)
    prev_country = country

    # temporarily converts the input into a dataframe, for column manipulation
    input_df = pd.DataFrame(input_list, columns=['weight', 'index', 'x',
                                                 'group'])
    # compute the sum of the weights and store it as the weight value for Total
    input_df.at[15, 'weight'] = sum(input_df.loc[0:14, 'weight'])
    input_df.at[15, 'group'] = "Total"
    input_df = input_df.drop(columns='x')  # drop an extraneous column
    input_df["yr_month"] = data_date  # all 16 rows of new column get same date
    input_df["un_cntry"] = country
    input_df["city"] = city

    if country not in iso_dict:  # verify each country has an ISO code to use
        has_valid_iso = False
        input_iso = ''

        while not has_valid_iso:  # collect user input for any missing ISO codes
            input_iso = input("Enter an ISO Alpha 3 code for " + country + ": ")
            if len(input_iso) != 3:
                print("Invalid ISO code.  Must be 3 characters in length")
            else:
                has_valid_iso = True

        iso_dict.update({country: input_iso.upper()})
        # in addition to updating iso_dict, we save any new ISO codes in a csv
        with open(COUNTRY_TO_ISO_FILE, 'a', newline='') as fd:
            writer = csv.writer(fd)
            writer.writerow([country, input_iso.upper()])

    # add the iso code column, making use of the updated iso_dict
    input_df["iso_a3"] = iso_dict[country]

    # for the common country name column, we just look up the iso code in a
    # dictionary where the ISO codes are keys and the common country names
    # from the ISO codes spreadsheet are values
    if iso_dict[country] not in reverse_iso_dict:
        has_valid_country = False
        input_country = ''

        while not has_valid_country:  # collect user input for missing countries
            input_country = input("Enter common country name for ISO code "
                                  + iso_dict[country] + ": ")
            c = input("Confirm that country name " + input_country + "will be "
                      + "assigned to ISO code " + iso_dict[country] + " (Y/N): ")
            if c.upper() == 'Y':
                has_valid_country = True
            else:
                print("Try again.")

        reverse_iso_dict.update({iso_dict[country]: input_country})
        # in addition to updating iso_dict, we save any new ISO codes in a csv
        with open(ISO_TO_COUNTRY_FILE, 'a', newline='') as fd:
            writer = csv.writer(fd)
            writer.writerow([iso_dict[country], input_country])

    input_df["cmn_cntry"] = reverse_iso_dict[iso_dict[country]]

    # looks up category names in cat_dict to grab corresponding category codes
    for grp in input_df['group'].tolist():
        if grp not in cat_dict:
            has_valid_cat_code = False
            input_cat_code = ''

            # collect user input for any missing category codes
            while not has_valid_cat_code:
                print("Existing category codes:")
                print(cat_dict)
                input_cat_code = \
                    input("Enter a category code for : ").upper()
                if len(input_cat_code) == 4:
                    break
                print("Invalid category code - must be 4 characters in length")

            # save any new category codes to cat_dict and to csv
            with open(CAT_CODE_FILE, 'a', newline='') as fd:
                writer = csv.writer(fd)
                writer.writerow([grp, input_cat_code])
            cat_dict.update({grp: input_cat_code})

    input_df['cat_code'] = input_df['group'].map(cat_dict)
    input_df['unique_id'] = \
        input_df['yr_month'] + '_' + input_df['iso_a3'] + '_' + input_df[
            'cat_code']

    # orders columns according to column_names and replaces 0's with null values
    return input_df.loc[:, column_names]. \
        replace(0, float("nan")).values.tolist()


# Loops through the duty station place names in a given spreadsheet, passing
# each block of cell values that populates on the sheet into arrange_data().
# These results are appended together in order to write each year-month csv,
# and they are also used to update the global variables that will become the
# mega-csv, the pivoted csv, and the data extent csv.
def generate_flat_csv(file_name):
    input_book_name = file_name
    global aggregate_list, extent

    # initialize the output dataframe with columns in the desired order
    output = []

    # open the workbook and the Control sheet, and read its date and place names
    book = excel_app.books.open(SHEETS_PATH + '/' + input_book_name)
    sheet = book.sheets['Control']

    # locates the cell containing the dataset date for the current spreadsheet,
    # based on a list of several possible cell addresses
    data_date_found = False
    for c in DATA_DATE_CELLS:
        if isinstance(sheet.range(c).value, datetime):
            data_date = sheet.range(c).value.strftime('%Y_%m')
            data_date_found = True
            break

    if not data_date_found:
        print("Could not find dataset date in spreadsheet " + input_book_name)
        print("Please manually locate the dataset date cell address and add it "
              "to the DATA_DATE_CELLS list in " + __file__)
        exit_processing_early()

    # reads in the column of place names as a list and checks the first and last
    # values to ensure they are formatted as expected
    place_names = book.sheets['Aggregation'] \
        .range(PLACE_NAMES_START_CELL).expand('down').value
    if " >> " not in place_names[0]:
        print("Unexpected value in place names start cell for " + data_date)
        exit_processing_early()
    elif " >> " not in place_names[-1]:
        place_names.pop()
        if " >> " not in place_names[-1]:
            print("Unexpected value at end of places list for " + data_date)
            exit_processing_early()

    # verifies the location of the cell where place names are pasted
    if " >> " not in sheet.range(PLACE_NAME_WRITE_CELL).value:
        print("Warning: unexpected value in PLACE_NAME_WRITE_CELL " + data_date)
        exit_processing_early()

    for pn in place_names:
        if '>>' not in pn and pn not in ['Dominican Republic', 'New Caledonia']:
            print("Unexpected place name " + pn + " in " + data_date)
            exit_processing_early()
        if pn[:3] == 'USA' and 'New York' in pn:
            continue

        before_length = len(output)

        # paste each place name into the cell, grab the data that populates as
        # a result of that, pass that data into arrange_data, and append result
        sheet.range(PLACE_NAME_WRITE_CELL).value = pn

        sum_of_nones = 0
        initial_data = sheet.range(DATA_READ_RANGE).value
        for cells in initial_data:
            sum_of_nones += cells.count(None)
        if sum_of_nones not in [3, 4]:
            print("Warning: missing data for " + pn + " in " + data_date
                  + ", skipping this record")
            continue  # skips this place name, doesn't read data for it
            # print("Warning: unexpected DATA_READ_RANGE for " + pn + " in " +
            #       data_date)
            # exit_processing_early()

        input_list = initial_data
        arranged = arrange_data(input_list, pn, data_date)
        output.extend(arranged)

        # verify that 16 records have been appended for each place name
        if len(output) != before_length + 16:
            print("Warning: non-16 # of records for " + data_date + pn)

        # append the processed data to what will become the mega-csv
        aggregate_list.extend(arranged)

        # update the extent table, adding columns for any ISO codes or rows
        # for any dataset dates that aren't yet in the table, and marking an 'x'
        # in every table cell for which data was recorded for the corresponding
        # dataset date and ISO code.
        common_country = reverse_iso_dict[iso_dict[pn.split('>>')[0].strip()]]
        # we already updated these dictionaries in arrange_data()
        if common_country not in extent.columns:
            extent[common_country] = None  # new column
        if data_date not in extent.index.names:
            extent.append(pd.Series(name=data_date, dtype='str'))  # new row
        extent.at[data_date, common_country] = 'x'

    # write each year-month csv to the output_csvs folder
    new_file_name = data_date + '_un_icsc_rpid.csv'
    output_df = pd.DataFrame(output, columns=column_names)
    output_df.to_csv('output_csvs/yr_month_csvs/' + new_file_name,
                     index=False, encoding='utf-8-sig')

    # add the name of the just-processed spreadsheet to the list of files for
    # which processing is complete
    with open(ALREADY_DONE_FILE, 'a', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow([input_book_name])

    book.close()  # close the spreadsheet that's currently open


# Writes updated data to the mega-csv, pivoted csv, and data extent files.
def update_aggregate_csvs():
    aggregate_df = pd.DataFrame(aggregate_list[1:], columns=column_names) \
        .drop_duplicates(subset=['unique_id'], keep='last')

    # setting the cat codes column as a "category" field allows us to specify
    # how they should be sorted.  In this case, they are sorted according to
    # their order in cat_list.
    aggregate_df['cat_code'] = aggregate_df['cat_code'].astype('category') \
        .cat.set_categories(cat_list)
    sorted_df = aggregate_df.sort_values(by=['yr_month', 'iso_a3', 'cat_code'])
    sorted_df.to_csv(MEGA_FILE, index=False, encoding='utf-8-sig')

    # pivot the mega-csv so that each category code becomes a separate column,
    # with the corresponding weight and index as sub-columns
    to_pivot_df = sorted_df.drop(columns=['unique_id', 'group'])
    pivot_df = to_pivot_df.pivot(index=column_names[1:6],
                                 columns='cat_code', values=['weight', 'index'])
    # collapses the multi-level columns into a single set of columns,
    # concatenating the category code with either "_idx" or "_wgt" for the index
    # or weight
    pivot_df.columns = [col[1].lower() + '_' + abbrev_dict[col[0]] for col in
                        pivot_df.columns.values]
    # the original pivot operation converted several columns into named indices
    indices_to_columns(pivot_df)  # this converts them back to columns
    # add a unique_id column concatenating the year-month and the ISO code
    pivot_df.insert(0, 'unique_id',
                    pivot_df['yr_month'] + '_' + pivot_df['iso_a3'])
    pivot_df.to_csv(PIVOTED_FILE, index=False, encoding='utf-8-sig')

    # writes the extent table to csv after sorting the rows by dataset date
    extent.sort_index().to_csv(EXTENT_FILE, index=True, encoding='utf-8-sig')


# Updates aggregate files and exits script.  Used when script encounters
# unexpected values that it cannot fix itself.
def exit_processing_early():
    update_aggregate_csvs()
    excel_app.quit()
    sys.exit()


# *************** READY TO RUMBLE *****************

# The two-line block of code below will close out zombie Excel instances from
# any script runs that errored out before excel_app.quit() could be called. If
# one of the spreadsheets is telling you that it's read-only, uncomment those
# two lines, comment out everything below it, and run the script, and
# afterwards, you should be able to open the spreadsheet.

# for a in xw.apps:
#     a.quit()

# verify that the needed files are present in their expected folder locations
paths_to_check = [ALREADY_DONE_FILE, MEGA_FILE, PIVOTED_FILE, EXTENT_FILE,
                  CAT_CODE_FILE, COUNTRY_TO_ISO_FILE, ISO_TO_COUNTRY_FILE]
missing_paths = []
for path in paths_to_check:
    if not os.path.exists(path):
        missing_paths.append(path)
if missing_paths:
    print("The following files are missing or have been moved:\n"
          + str(missing_paths) + "\nPlease restore these files to their "
          + "locations or create new versions, as described in\n"
          + "http://gisdatalib.digitalscholarship.brown.edu/doku.php?id=data:un_icsc")
    excel_app.quit()
    sys.exit()

# verify that the input spreadsheets folder is in its expected location
if not os.path.exists(SHEETS_PATH):
    print("Could not locate the folder for input spreadsheets.  Please repair "
          + "the file structure, \nor edit SHEETS_PATH in this script to work "
          + "with a different file structure, as described in\n"
          + "http://gisdatalib.digitalscholarship.brown.edu/doku.php?id=data:un_icsc")
    excel_app.quit()
    sys.exit()

# read in the file names of spreadsheets that have previously been processed
already_done_file_names = []
with open(ALREADY_DONE_FILE) as f:
    reader = csv.reader(f)
    for row in reader:
        for item in row:
            already_done_file_names.append(item)

# read in the file names of every spreadsheet in the designated input folder
input_file_names = []
for (dirpath, dirnames, filenames) in os.walk(SHEETS_PATH):
    input_file_names.extend(filenames)

# determine which file names from the input folder, if any, need processing
spreadsheets_to_do = []
for file in input_file_names:
    # files starting with '~$' are Windows temporary files we don't want to open
    if file not in already_done_file_names and file[:2] != '~$':
        spreadsheets_to_do.append(file)
if spreadsheets_to_do:
    print(str(len(spreadsheets_to_do)) + " new files detected.  Processing...")
    initialize_dictionaries()  # reads already-processed data & ISO/cat codes

    for s in spreadsheets_to_do:
        generate_flat_csv(s)  # reads spreadsheets & produces corresponding csvs

    update_aggregate_csvs()  # updates aggregate files with new data
else:  # if there are no spreadsheets to do, give user option to re-process all
    print("No new files detected.  To re-process old files, open "
          + "already_done_file_list.csv \nand delete the rows corresponding "
          + "to the spreadsheets you want to re-do, then \nsave and close it "
          + "and try running this script again.\n")
print("Processing complete.")

# close out our virtual Excel instance
excel_app.quit()
