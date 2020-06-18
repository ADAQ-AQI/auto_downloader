"""
Configuration file for auto_downloader.

Change settings in this file to change search and download settings
for air quality data files.
"""
# Enter your email address here so that data can be sent to you:
MY_EMAIL = "corinne.bosley@metoffice.gov.uk"

# Choose one of the following download methods and comment out the other one.
# Direct download is not available for Scottish data.
DOWNLOAD_METHOD = "email"
# DOWNLOAD_METHOD = "direct"

# Choose your list of dates.  I've made these timechunks quite small so that
# data requests don't exceed the size limit, but you can biggen if you want
# less emails.  It's really a balancing act.
DATES_LIST = [["2000", "2000"],
              ["2001", "2001"],
              ["2002", "2003"],
              ["2004", "2005"],
              ["2006", "2007"],
              ["2008", "2009"],
              ["2010", "2011"],
              ["2012", "2013"],
              ["2014", "2015"],
              ["2016", "2017"],
              ["2018", "2019"],
              ["2020", "2020"]]

# These are the pollutants (or phenomena) for which to collect data.
# The strings are very specific, and must only change if the names or values
# on the respective websites change.
# You may of course add or comment out pollutants according to your needs,
# but they must mirror the names and values of those in the website lists.
SCOTTISH_PHENOM_DICT = {"PM10 particulate matter (Hourly measured)": "V10",
                        "PM2.5 particulate matter (hourly measured)": "V25",
                        "Ozone": "O3",
                        "Nitric oxide": "NO",
                        "Nitrogen dioxide": "NO2",
                        "Nitrogen oxides as nitrogen dioxide": "NOX as NO2",
                        "Sulphur dioxide": "SO2",
                        "Carbon monoxide": "CO"}

WELSH_PHENOM_DICT = {"Particulates < 10um (hourly measured)": "GE10",
                     "Particulates < 2.5um (Hourly measured)": "PM25",
                     "Ozone": "O3",
                     "Nitric oxide": "NO",
                     "Nitrogen dioxide": "NO2",
                     "Nitrogen oxides as nitrogen dioxide": "NOX as NO2",
                     "Sulphur dioxide": "SO2",
                     "Carbon monoxide": "CO"}

# NIRISH_PHENOM_LIST =
