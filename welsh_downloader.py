"""
Script to try and download Welsh air quality data files automatically.

Requirements are as follows:

The data we would like from each website is:

Raw measurement data (i.e. not daily means, etc) from the automatic monitoring
networks – this should be hourly data for our 8 key pollutants:
Ozone,
Nitric Oxide,
Nitrogen dioxide,
Nitrogen oxides as nitrogen dioxide,
Sulphur dioxide,
Carbon monoxide,
Particulates < 10um (hourly measured),
Particulates < 2.5um (hourly measured)
(Data for all available monitoring sites
Data for each year from 2000 onwards)

Ideally the data in a CSV format or similar – not essential, so long as it is
in a format that we can easily read and process into the same form as other
observational data
"""

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from config import MY_EMAIL, DATES_LIST
from utils import driver, select_option

PHENOM_DICT = {"Particulates < 10um (hourly measured)": "GE10",
               # "Particulates < 2.5um (Hourly measured)": "PM25",
               # "Ozone": "O3",
               # "Nitric oxide": "NO",
               # "Nitrogen dioxide": "NO2",
               # "Nitrogen oxides as nitrogen dioxide": "NOX as NO2",
               # "Sulphur dioxide": "SO2",
               # "Carbon monoxide": "CO"
}


def click_next(page):
    next_button_xpath = '/html/body/div/div/div/div/div[1]/div/div/div[2]/' \
                        'section/div/div[2]/div/div/div[1]/form/input[' \
                        + page + ']'

    next_button = driver.find_element_by_xpath(next_button_xpath)
    next_button.click()
    return


# Navigate to starting page:
start_url = "https://airquality.gov.wales/maps-data/data-selector/index"
driver.delete_all_cookies()
# driver.implicitly_wait(30)

for (key, value) in PHENOM_DICT.items():
    for timechunk in DATES_LIST:
        print("Searching for {} data for {} to {}...".format(key,
                                                             timechunk[0],
                                                             timechunk[1]))
        driver.get(start_url)

        # Set options for parameter group and type of data:
        # "Automatic Monitoring Data" == "4"
        select_option("f_group_id", "Automatic Monitoring Data",
                      spare_value="4")

        select_option("action", "Measurement data and simple statistics")

        # Submit request:
        click_next('3')
        # ---------------------------------------------------------------------

        # Move to next page, select options for phenomenon here:
        # "phenom" == key (see dictionary)
        phenom = driver.find_element_by_id("f_parameter_id")
        select = Select(phenom)
        select.deselect_all()
        select.select_by_visible_text(key)

        click_next('3')
        # ---------------------------------------------------------------------

        # Move to next page, select options for statistic type here:
        select_option("f_statistic_type_id", "Measured Data",
                      spare_value="9999")
        click_next('4')
        # ---------------------------------------------------------------------

        # Move to next page, select options for date range here:
        select_option("date-choice", "Custom")

        start = "01/01/" + timechunk[0]
        start_date = driver.find_element_by_id("custom-date-start")
        start_date.send_keys(start)

        end = "31/12/" + timechunk[1]
        end_date = driver.find_element_by_id("custom-date-end")
        end_date.send_keys(end)

        click_next('4')
        # ---------------------------------------------------------------------

        # Move to next page, select options for sub-region here:
        select_option("f_region_id", "All", spare_value="9999")
        click_next('4')
        # ---------------------------------------------------------------------

        # Move to next page, select monitoring sites here:
        select_option("ds[s][site][]", "All", spare_value="9999")
        click_next('3')
        # ---------------------------------------------------------------------
# TODO: Form the following statement to catch errors and only proceed if there is no error
# TODO: Decide whether to download CSV files directly or have them emailed.
        # Check for any errors in the data request, then proceed accordingly:
        try:
            driver.find_element_by_class_name("error")
            print("Data for {} between {} and {} too large; "
                  "please download manually in chunks smaller "
                  "than 5 years.".format(key, timechunk[0], timechunk[1]))
            # Save a screenshot of the confirmation page to check data:
            filename = str("denied_requests/welsh/request_" + key +
                           timechunk[0] + timechunk[1] + ".png")
        except selenium.common.exceptions.NoSuchElementException:
            filename = str("confirmations/welsh/download_confirmation_" + key +
                           timechunk[0] + timechunk[1] + ".png")
        driver.save_screenshot(filename)

driver.close()
print("Finished! Please check your output folders for anything unexpected.")


