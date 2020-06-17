"""
Toy to try and download data files daily.  Method as yet unknown.

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

from config import MY_EMAIL, DATES_LIST, PHENOM_DICT


def select_option(menu_id, selection, spare_value=None):
    try:
        element = driver.find_element_by_id(menu_id)
    except selenium.common.exceptions.NoSuchElementException:
        try:
            element = driver.find_element_by_name(menu_id)
        except selenium.common.exceptions.NoSuchElementException:
            try:
                element = driver.find_element_by_name(menu_id + "[]")
            except selenium.common.exceptions.NoSuchElementException:
                print("Tried finding element every way I can, not sure what "
                      "else to do...")
                pass

    select = Select(element)
    try:
        select.select_by_visible_text(selection)
    except selenium.common.exceptions.NoSuchElementException:
        try:
            select.select_by_value(selection)
        except selenium.common.exceptions.NoSuchElementException:
            try:
                select.select_by_visible_text(spare_value)
            except selenium.common.exceptions.NoSuchElementException:
                try:
                    select.select_by_value(spare_value)
                except selenium.common.exceptions.NoSuchElementException:
                    print("There is a problem with this selection; "
                          "please see input lists for details.")
                    pass
    return


def _find_date_field(field_name, target):
    date_field = driver.find_element_by_name(field_name)
    select = Select(date_field)
    select.select_by_visible_text(target)
    return


def set_dates(start_date, end_date):
    # Move to next page, select options for date range here:
    # NOTE: Due to download size limitations, we must download these files
    # in 5-year chunks.
    _find_date_field("f_start_day", "01")
    _find_date_field("f_start_month", "01")
    _find_date_field("f_start_year", start_date)

    _find_date_field("f_end_day", "31")
    _find_date_field("f_end_month", "12")
    _find_date_field("f_end_year", end_date)

    step4_button = driver.find_element_by_name("go")
    try:
        step4_button.click()
    except:
        print("It looks like there was a problem collecting {} data for "
              "dates between 01/01/{} and 31/12/{}. Please consult browser "
              "for details and download manually if required.".format
              (key, timechunk[0], timechunk[1]))
        pass


# Navigate to starting page:
start_url = "http://www.scottishairquality.scot/data/data-selector"
driver = webdriver.Firefox()
driver.delete_all_cookies()

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

        # "Measurement data and simple statistics" == "step1"
        select_option("action", "Measurement data and simple statistics")

        # Submit request:
        step1_button = driver.find_element_by_name("go")
        step1_button.click()
        # ---------------------------------------------------------------------
        # TODO: Fix this!!
        # Move to next page, select options for phenomenon here:
        # "phenom" == key (see dictionary)
        driver.find_element_by_id("f_parameter_id").send_keys(key)

        step2_button = driver.find_element_by_name("go")
        step2_button.click()
        # ---------------------------------------------------------------------

        # Move to next page, select options for region and data type here:
        # # "Select All" == "9999"
        select_option("f_sub_region_id", "Select All", spare_value="9999")

        # "Measured Data" == "9999"
        select_option("f_statistic_type_id", "Measured Data",
                      spare_value="9999")

        step3_button = driver.find_element_by_name("go")
        step3_button.click()
        # ---------------------------------------------------------------------

        # Move to next page, set start and end dates for dataset here:
        set_dates(timechunk[0], timechunk[1])
        # ---------------------------------------------------------------------

        # Move to next page, select options for data collection sites here:
        # # "Select All" == "9999"
        try:
            select_option("f_site_id", "Select All")
        except UnboundLocalError:
            print("Unable to find any sites for {} data in this region for "
                  "dates between {} and {}. Skipping phenomenon to continue "
                  "data search...".format(key, timechunk[0], timechunk[1]))
            # Save a screenshot of the confirmation page to check data:
            filename = str("errors/error_" + key +
                           timechunk[0] + timechunk[1] + ".png")
            confirmation = driver.save_screenshot(filename)
            break

        step5_button = driver.find_element_by_name("go")
        step5_button.click()
        # ---------------------------------------------------------------------

        # Move to confirmation page, enter email address to receive data:
        enter_email = driver.find_element_by_name("f_email")
        enter_email.send_keys(MY_EMAIL)

        # Save a screenshot of the confirmation page to check data:
        filename = str("confirmations/download_confirmation_" + key +
                       timechunk[0] + timechunk[1] + ".png")
        confirmation = driver.save_screenshot(filename)

        # Confirm and get data:
        get_data = driver.find_element_by_name("go")
        get_data.click()

        try:
            confirm = driver.find_element_by_tag_name("h3")
        except selenium.common.exceptions.NoSuchElementException:
            print("Data for {} between {} and {} too large; "
                  "please download manually in chunks smaller "
                  "than 5 years.".format(key, timechunk[0], timechunk[1]))
            driver.back()
            # Save a screenshot of the confirmation page to check data:
            filename = str("denied_requests/request_" + key +
                           timechunk[0] + timechunk[1] + ".png")
            confirmation = driver.save_screenshot(filename)
            break

driver.close()
print("Finished! Please check your output folders for anything unexpected.")
