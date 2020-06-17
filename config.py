"""
Configuration file for auto_downloader.

Change settings in this file to change search and download settings
for air quality data files.
"""

MY_EMAIL = "corinne.bosley@metoffice.gov.uk"

DATES_LIST = [["2000", "2004"],
              ["2005", "2009"],
              ["2010", "2014"],
              ["2015", "2019"],
              ["2020", "2020"]]

PHENOM_DICT = {"PM10 particulate matter (Hourly measured)": "V10",
               "PM2.5 particulate matter (Hourly measured)": "V25",
               "Ozone": "O3",
               "Nitric oxide": "NO",
               "Nitrogen dioxide": "NO2",
               "Nitrogen oxides as nitrogen dioxide": "NOX as NO2",
               "Sulphur dioxide": "SO2",
               "Carbon monoxide": "CO"}
