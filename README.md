This dataset is a time series of retail price indices that reflect the relative costs of various categories of goods and services experienced by United Nations (UN) staff at duty stations around the world.

This page was last updated on July 6, 2023.  The most recent update includes data from January 2004 through December 2022.

## Access

The data files in this repository are licensed under a [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/).  Specifically, they are to be used for non-commercial research purposes, they cannot be redistributed or republished, and the United Nations International Civil Service Commission (UN ICSC) must be cited as a source when the data is used for research.  

The following products are available for viewing or download:

* all data from 2004 through the present in a [long format](https://github.com/Brown-University-Library/geodata_un_retail_idx/blob/main/final_data/aggregate_files/all_un_icsc_rpid.csv) 
* all data from 2004 through the present in a [wide format](https://github.com/Brown-University-Library/geodata_un_retail_idx/blob/main/final_data/aggregate_files/all_un_icsc_rpid_pivoted.csv) 
* [Individual .csv files for particular year-month snapshots](https://github.com/Brown-University-Library/geodata_un_retail_idx/tree/main/final_data/year_month_files) 
* A [data extent file](https://github.com/Brown-University-Library/geodata_un_retail_idx/blob/main/final_data/aggregate_files/data_extent.csv) listing the specific dates for which retail price index data is available for each country in the dataset.

The UN ICSC are the original creators of this data, and they have requested that prospective users provide basic information about themselves and their anticipated uses of this data using the [Request Access button on their website.](https://icsc.un.org/Home/DataRPI)  Requesting access also gives users access to the original spreadsheet files that were used to generate this dataset.

_Disclaimer: Every effort was made to insure that the data, which was compiled from public sources, was processed and presented accurately. The creators and Brown University disclaim any liability for errors, inaccuracies, or omissions that may be contained therein or for any damages that may arise from the foregoing. Users should independently verify the accuracy and fitness of the data for their purposes._

## Documentation

The retail price indices in this dataset are officially called Post Adjustment Indices (PAI), and the UN ICSC creates them for a specific purpose: adjusting the salaries of UN staff around the world based on variations in the cost of living.  They make PAI data publicly available on a [dedicated website](https://unicsc.org/Home/DataRPI), because the information about costs of living around the world reflected in these indices could be useful for research or other purposes. 

Data is published six times a year (Feb-Apr-Jun-Aug-Oct-Dec) from 2009 to the present. Prior to that time, data was published four times a year (Mar-Jun-Sep-Dec) and the transition occurred midway through 2008, which has five data points (Mar-Jun-Aug-Oct-Dec). On the UN ICSC website, data for each year-month snapshot in time is stored in a separate Excel spreadsheet.  Additionally, access to the Retail Price Indices with Details (RPID) spreadsheets, which break down retail price indices into several components reflecting different categories of goods or services, requires signing up for an account, even though it's publicly available.

The GIS and Data Services team at the Brown University library has set up a script-based workflow for converting the data from the UN ICSC RPID spreadsheets into formats that are more conducive to analysis over space and time.  Visit the [processing folder of this repository](https://github.com/Brown-University-Library/geodata_un_retail_idx/tree/main/processing) for more details on the script.

There are two basic data points that are recorded for each retail category in a given country at a particular point in time: a numerical index and a "weight" value.  Roughly speaking, each weight value represents the US Dollar nominal monthly expenditures by an average staff member at a country's UN duty station for a given retail category, based on surveys of UN staff conducted by the ICSC.  Each index value indicates relative differences in costs for a given retail category at a duty station compared to costs in New York (the UN headquarters), taking into account price levels, local inflation patterns, and exchange rates.  Index values less than 100 indicate that costs for a given retail category at a given duty station are lower than they are in New York, and index values higher than 100 reflect the reverse.  

For a more accurate and detailed breakdown of what weight and index numbers represent and how they are calculated, please consult the [United Nations Post Adjustment System methodology document](https://github.com/Brown-University-Library/geodata_un_retail_idx/blob/main/original_data/PABooklet.pdf) produced by the UN ICSC.

The [long-formatted .csv file](https://github.com/Brown-University-Library/geodata_un_retail_idx/blob/main/final_data/aggregate_files/all_un_icsc_rpid.csv) containing all of the data from 2004 to the present is organized with the following columns:

| column    | description                                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------ |
| unique_id | a combination of yr_month, iso_a3, and cat_code that uniquely identifies each row (i.e. 2004_09_PAK_FOOD)    |
| yr_month  | YYYY_MM (i.e. 2004_09 for September 2004)                                                                    |
| iso_a3    | the ISO 3166 Alpha 3 code that uniquely identifies the country of the duty station (i.e. PAK for Pakistan)   |
| cmn_cntry | the "common name" of the country, corresponding with its ISO 3166 Alpha 3 code                               |
| un_cntry  | the "UN name" of the country (how the country was named by the UN in the original spreadsheet for that time) |
| city      | the city where the UN duty station for the country is located                                                |
| cat_code  | a four-letter code corresponding to a particular retail price category (see below for full list)             |
| group     | the full name of the retail price category                                                                   |
| weight    | US Dollar nominal monthly expenditure by an average UN staff member                                          |
| index     | numerical Post Adjustment Index value                                                                        |

Therefore, each row of the long-formatted file uniquely identifies a given category for a given duty station at a given time.  The [individual files for particular year-month snapshots](https://github.com/Brown-University-Library/geodata_un_retail_idx/tree/main/final_data/year_month_files) have the same column format.  In the [wide-formatted .csv file](https://github.com/Brown-University-Library/geodata_un_retail_idx/blob/main/final_data/aggregate_files/all_un_icsc_rpid_pivoted.csv), each row has all the index data for a given country at a given time, and the category codes are pivoted into separate columns.  For each four-letter category code (i.e. HOUS for housing-related costs), there is one column in the wide csv file for its corresponding weight (i.e. “HOUS_wgt”) and another column for its corresponding index (i.e. “HOUS_idx”). 

The retail category names and corresponding four-character category codes are as follows:

| cat_code | group                                                               |
| -------- | ------------------------------------------------------------------- |
| FOOD     | Food And Non-alcoholic Beverages                                    |
| ALCO     | Alcoholic Beverages And Tobacco                                     |
| CLTH     | Clothing And Footwear                                               |
| HOUS     | Housing, Water, Electricity, Gas And Fuels                          |
| FURN     | Furniture, Household Equipment And Routine Maintenance Of The House |
| HEAL     | Health                                                              |
| TRNS     | Transport                                                           |
| COMM     | Communication                                                       |
| CLTR     | Recreation And Culture                                              |
| EDUC     | Education                                                           |
| RHTL     | Restaurants And Hotels                                              |
| MISC     | Miscellaneous Goods And Services                                    |
| MEDI     | Medical Insurance                                                   |
| PNSN     | Pension Contribution                                                |
| OUTA     | Out Area                                                            |
| TOTL     | Total                                                               |

"Out Area" (a.k.a "out-of-area") reflects expenses by UN staff on goods or services outside the country of their duty station assignment.  The dollar weight values for this category will vary by duty station and over time, but the index value will always be 100, since this category represents international expenditures converted to US dollars rather than expenses that reflect local cost conditions of the duty station.  

The pension contribution category is also unique, as all UN staff pay a fixed US dollar amount in pension contributions.  This means that in addition to always having an index value of 100, the pension contribution category will list the same dollar weight value for all duty stations for a given time.  

The [United Nations Post Adjustment System methodology document](https://github.com/Brown-University-Library/geodata_un_retail_idx/blob/main/original_data/PABooklet.pdf) contains more details on how these categories are determined, and how "total" index values for each duty station at a given time are calculated.

![](un_rpid_map_feb2022.png)