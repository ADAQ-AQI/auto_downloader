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

from config import MY_EMAIL, DATES_LIST, WELSH_PHENOM_DICT, DOWNLOAD_METHOD
from utils import driver, select_option


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

for (key, value) in WELSH_PHENOM_DICT.items():
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
        try:
            select.select_by_visible_text(key)
        except selenium.common.exceptions.NoSuchElementException:
            select.select_by_value(value)

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

        # Check for any errors in the data request, then proceed accordingly:
        try:
            # If there is an error, take a screenshot then move on:
            driver.find_element_by_class_name("error")
            print("Data for {} between {} and {} too large; "
                  "please download manually in chunks smaller "
                  "than 5 years.".format(key, timechunk[0], timechunk[1]))
            # Save a screenshot of the confirmation page to check data:
            filename = str("denied_requests/welsh/request_" + key +
                           timechunk[0] + timechunk[1] + ".png")
            driver.save_screenshot(filename)
            break
        except selenium.common.exceptions.NoSuchElementException:
            # If there is no error, take a screenshot of the confirmation,
            # then carry out appropriate download method:
            filename = str("confirmations/welsh/download_confirmation_" + key +
                           timechunk[0] + timechunk[1] + ".png")
            driver.save_screenshot(filename)
            if DOWNLOAD_METHOD == "email":
                enter_email = driver.find_element_by_name("ds[p][output]")
                enter_email.send_keys(MY_EMAIL)
                tickbox = driver.find_element_by_name("accept")
                tickbox.click()
                send_xpath = "/html/body/div/div/div/div/div[1]/" \
                             "div/div/div[2]/section/div/div[2]/" \
                             "div/div/div[2]/div/div[1]/div[2]/" \
                             "div[2]/form/input[3]"
                send = driver.find_element_by_xpath(send_xpath)
                send.click()
            elif DOWNLOAD_METHOD == "direct":
                download_xpath = "/html/body/div/div/div/div/div[1]/" \
                                 "div/div/div[2]/section/div/div[2]/" \
                                 "div/div/div[2]/div/div[1]/div[2]/" \
                                 "div[1]/a"
                download_csv = driver.find_element_by_xpath(download_xpath)
                download_csv.click()
            else:
                print("No valid download method supplied; please check "
                      "configuration file for settings.")

driver.close()
print("Finished! Please check your output folders for anything unexpected.")


