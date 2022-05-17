This dataset is a time series of retail price indices for various categories of goods and services that reflect the relative cost-of-living of United Nations (UN) international staff stationed at duty stations around the world.

This page was last updated on May 17, 2022, with retail price index data available from January 2004 through December 2021.

## Access

The data files in this page are licensed under a [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/).  Specifically, they are to be used for non-commercial research purposes, they cannot be redistributed or republished, and the United Nations International Civil Service Commission (UN ICSC) must be cited as a source when the data is used for research.  

The full time series is available as a .csv file in either a [long](https://github.com/Brown-University-Library/geodata_un_retail_idx/blob/main/final_data/aggregate_files/all_un_icsc_rpid.csv) or a [wide](https://github.com/Brown-University-Library/geodata_un_retail_idx/blob/main/final_data/aggregate_files/all_un_icsc_rpid_pivoted.csv) format.  [Individual .csv files for particular year-month snapshots](https://github.com/Brown-University-Library/geodata_un_retail_idx/tree/main/final_data/year_month_files) are also available for viewing or download.  Data availability varies by country over time; see the [full data extent file](https://github.com/Brown-University-Library/geodata_un_retail_idx/blob/main/final_data/aggregate_files/data_extent.csv) for details.

## Documentation

The UN ICSC originally created these retail price indices in order to adjust the salaries of UN staff around the world based on variations in the cost of living.  However, they also publish these data on a [dedicated website](https://unicsc.org/Home/DataRPI) so that the information they collect about the costs of living around the world can be used by members of the public for research or other purposes.  However, the data on the UN ICSC website are only available in separate Excel spreadsheets for particular snapshots in time.  Additionally, access to the Retail Price Indices with Details (RPID) spreadsheets, which break down retail price indices by category of goods or services, requires signing up for an account, even though it's publicly available.

The GIS and Data Services team at the Brown University library has set up a script-based workflow for representing the data from the UN ICSC RPID spreadsheets in formats that are more conducive to analysis over space and time.  

In this dataset, there are two numbers recorded for each retail category in a given country at a particular point in time: the price index itself, and a weight value.  Roughly speaking, each weight value represents the US Dollar nominal monthly expenditures by an average staff member at the country's UN duty station for that retail category.  Each index value indicates relative differences in price levels and inflation for a given retail category at that duty station compared to New York, with values less than 100 indicating lower costs for that category than in New York and values higher than 100 reflecting higher costs than in New York.  

For a more accurate and detailed breakdown of what weight and index numbers represent and how they are calculated, please read the [United Nations Post Adjustment System pdf document](https://github.com/Brown-University-Library/geodata_un_retail_idx/blob/main/original_data/PABooklet.pdf) produced by the UN ICSC.

The flat .csv file representing the full dataset in long format contains the following columns of data:

^ column     ^ description                                                                                                   ^
| unique_id  | a combination of yr_month, iso_a3, and cat_code that uniquely identifies each row (i.e. 2004_09_PAK_FOOD)                            |
| yr_month   | YYYY_MM (i.e. 2004_09 for September 2004)                                                                     |
| iso_a3     | the ISO 3166 Alpha 3 code that uniquely identifies the country of the duty station                            |
| cmn_cntry  | the "common name" of the country, corresponding with its ISO 3166 Alpha 3 code                                |
| un_cntry   | the "UN name" of the country (how the country was named by the UN in the original spreadsheet for that time)  |
| city       | the city where the duty station for the country is located                                                    |
| cat_code   | a four-letter code corresponding to a particular index category                                             |
| group      | the full name of the index category                                                                           |
| weight     |                                                                                                               |
| index      |                                                                                                               |



The data is published six times a year (Feb-Apr-Jun-Aug-Oct-Dec) from 2009 to present. Prior to that time, data was published four times a year (Mar-Jun-Sep-Dec) and the transition occurred midway through 2008 which has five data points (Mar-Jun-Aug-Oct-Dec).

There are two sets of files:

Retail Price Index (RPI) covers March 1997 to the present and contains a summary for each country with the name of the duty station city, an exchange rate, local currency, a total retail index, and a total index that excludes housing. Data from March 2002 to present are stored in two identical files, an Excel spreadsheet and a PDF. Prior to 2002 a mix of PDF, DOC, and plain text files (stored with the extension PRN) were used. The older .xls format was used from Mar 2002 to Aug 2013, and the modern .xlsx format is used from Dec 2013 to present.

Retail Price Index with Details (RPID) covers December 2002 to the present. Data for each year-month is stored in an Excel spreadsheet with a macro that allows you to choose a single country / duty station and see how the total index for each country was weighted for different retail categories. Each spreadsheet has one worksheet for the macro (“Control”) and a second worksheet that lists the total index for all countries for that time (“Aggregation”). The older .xls format was used from March 2002 to August 2013, and the modern .xlsm format is used from December 2013 to present. The files for December 2002 to September 2003 are password protected and can't be opened, and the file for December 2003 displays index values but not their corresponding weights. 

The data is published six times a year (Feb-Apr-Jun-Aug-Oct-Dec) from 2009 to present. Prior to that time, data was published four times a year (Mar-Jun-Sep-Dec) and the transition occured midway through 2008 which has five data points (Mar-Jun-Aug-Oct-Dec).  Data availability varies by country; see the [full data extent file](https://github.com/Brown-University-Library/geodata_un_retail_idx/blob/main/final_data/aggregate_files/data_extent.csv) for details.

Roughly speaking, each weight value represents the US Dollar nominal monthly expenditures by an average staff member for a given spending category, and each index value represents the relative difference between costs for that spending category at that duty station and costs in New York (an index of 100 means costs are equal to that of New York at that time).  For a more accurate and detailed breakdown of what weight and index numbers represent and how they are calculated, please read the methodology document entitled "United Nations Post Adjustment System" which is included in PDF format as part of this dataset (_geodata -> un_icsc -> original_data -> PABooklet.pdf).

The full list of columns in the year-month files and the mega file are as follows:




The full list of index categories and corresponding category codes are as follows:


^ cat_code  ^ group                                                                ^
| FOOD      | Food And Non-alcoholic Beverages                                     |
| ALCO      | Alcoholic Beverages And Tobacco                                      |
| CLTH      | Clothing And Footwear                                                |
| HOUS      | Housing, Water, Electricity, Gas And Fuels                           |
| FURN      | Furniture, Household Equipment And Routine Maintenance Of The House  |
| HEAL      | Health                                                               |
| TRNS      | Transport                                                            |
| COMM      | Communication                                                        |
| CLTR      | Recreation And Culture                                               |
| EDUC      | Education                                                            |
| RHTL      | Restaurants And Hotels                                               |
| MISC      | Miscellaneous Goods And Services                                     |
| MEDI      | Medical Insurance                                                    |
| PNSN      | Pension Contribution                                                 |
| OUTA      | Out Area                                                             |
| TOTL      | Total                                                                |

  
"Out Area" (a.k.a "out-of-area") reflects expenses by UN staff on goods or services outside the country of their duty station assignment.  The dollar weight values for this category will vary by duty station and over time, but the index value will always be 100, since this category represents international expenditures converted to US dollars rather than expenses that reflect local cost conditions of the duty station.  

The pension contribution category is also unique, as all UN staff pay a fixed US dollar amount in pension contributions.  This means that in addition to always having an index value of 100, the pension contribution category will list the same dollar weight value for all duty stations for a given time.  

Please read the “United Nations Post Adjustment System” methodology document for more details on how these categories are determined and how "total" index values for each station at a given time are calculated.