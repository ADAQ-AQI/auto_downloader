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

import requests
import os
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.keys import Keys

DATES_LIST = [["2000", "2004"],
              ["2005", "2009"],
              ["2010", "2014"],
              ["2015", "2019"],
              ["2020", "2020"]]

PHENOM_DICT = {"Ozone": "O3",
               "Nitric oxide": "NO",
               "Nitrogen dioxide": "NO2",
               "Nitrogen oxides as nitrogen dioxide": "NOX as NO2",
               "Sulphur dioxide": "SO2",
               "Carbon monoxide": "CO",
               "PM10 particulate matter (Hourly measured)": "V10",
               "PM2.5 particulate matter (Hourly measured)": "V25"}


def select_option(menu_id, selection, check=True):
    action_chains = ActionChains(driver)
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
    action_chains.move_to_element(element)
    action_chains.click()
    action_chains.pause(1)
    action_chains.send_keys_to_element(element, selection)
    action_chains.pause(1)
    action_chains.perform()
    if check is True:
        check_selection(element, menu_id, selection)
    return


def check_selection(element, menu_id, selection):
    # Check that correct box is in question:
    this_id = element.get_attribute("id")
    try:
        assert str(this_id) == str(menu_id)
    except AssertionError:
        this_name = element.get_attribute("name")
        try:
            assert str(this_name) == str(menu_id)
        except AssertionError:
            try:
                assert str(this_name) == str(menu_id + "[]")
            except AssertionError:
                print("Cannot find {} element anywhere. Moving on...")
                pass

    # Check that correct selection is in box:
    this_selection = element.get_attribute("value")
    try:
        assert str(this_selection) == str(selection)
    # selenium keeps sending the wrong keys to the box; if the wrong keys are
    # in the box now, try using 'Select All' or '9999' alternately:
    except AssertionError:
        print("option selected is {} where it should be {}. "
              "Resending value...".format(this_selection, selection))
        if selection == str("9999"):
            select_option(menu_id, "Select All")
        elif selection == str("Select All"):
            select_option(menu_id, "9999")
        else:
            print("There is a problem with selecting {} for {}, the "
                  "browser seems to want to select {}.  Please try manual "
                  "download instead.".format(selection,
                                             this_id,
                                             this_selection))
            pass

    return


def _find_date_field(field_name, offset, direction):
    date_field = driver.find_element_by_name(field_name)

    actions = ActionChains(driver)
    actions.click(date_field)
    n = 0
    if direction is "down":
        while n < int(offset):
            actions.key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN)
            n += 1
    elif direction is "up":
        while n < int(offset):
            actions.key_down(Keys.ARROW_UP).key_up(Keys.ARROW_UP)
            n += 1
    actions.__enter__()
    actions.perform()
    return


def set_dates(start_date, end_date):
    # Move to next page, select options for date range here:
    # NOTE: Due to download size limitations, we must download these files
    # in 5-year chunks.
    print("Entering dates between {} and {} ...".format(start_date, end_date))

    _find_date_field("f_start_day", 0, "down")
    _find_date_field("f_start_month", 0, "down")
    start_date_offset = 2020 - int(start_date)
    _find_date_field("f_start_year", start_date_offset, "up")

    _find_date_field("f_end_day", 31, "down")
    _find_date_field("f_end_month", 12, "down")
    end_date_offset = 2020 - int(end_date)
    _find_date_field("f_end_year", end_date_offset, "up")

    step4_button = driver.find_element_by_name("go")
    try:
        step4_button.click()
    except:
        print("It looks like there was a problem collecting {} data for "
              "dates between 01/01/{} and 31/12/{}. Please consult browser "
              "for details and download manually if required.".format
              (key, timechunk[0], timechunk[1]))
        pass


def set_data_type():
    # Select entries for drop-down menus on starting page:
    parameter_group = driver.find_element_by_id("f_group_id")
    # "Automatic Monitoring Data" = "4"
    select_option("f_group_id", "4")

    type_of_data = driver.find_element_by_name("action")
    # "Measurement data and simple statistics" = "step1"
    select_option("action", "step1")

    # Submit request:
    step1_button = driver.find_element_by_name("go")
    step1_button.click()


def set_phenom():
    parameter = driver.find_element_by_id("f_parameter_id")
    # "phenom" = "value" (see dictionary)
    select_option("f_parameter_id", value)

    step2_button = driver.find_element_by_name("go")
    step2_button.click()


def set_statistic_type():
    # region = driver.find_element_by_id("f_sub_region_id")
    # # "Select All" = "9999"
    # select_option("f_sub_region_id", "9999")

    data_type = driver.find_element_by_id("f_statistic_type_id")
    # "Measured Data" = "9999"
    select_option("f_statistic_type_id", "9999")

    step3_button = driver.find_element_by_name("go")
    step3_button.click()


def set_sites():
    # sites = driver.find_element_by_id("f_site_id")
    # # "Select All" = "9999"
    # select_option("f_site_id", "9999")

    step5_button = driver.find_element_by_name("go")
    try:
        step5_button.click()
    except:
        print("It looks like there was a problem collecting {} data for "
              "dates between 01/01/{} and 31/12/{}. Please consult browser "
              "for details and download manually if required.".format
              (key, timechunk[0], timechunk[1]))
        pass


# Navigate to starting page:
start_url = "http://www.scottishairquality.scot/data/data-selector"
driver = webdriver.Firefox()

for key, value in PHENOM_DICT.items():
    for timechunk in DATES_LIST:
        driver.get(start_url)
        # Set options for parameter group and type of data:
        set_data_type()
        # ---------------------------------------------------------------------
        # TODO: Fix this!!
        # Move to next page, select options for phenomenon here:
        print("Searching for {} data for {} to {}...".format(key,
                                                             timechunk[0],
                                                             timechunk[1]))

        set_phenom()
        # ---------------------------------------------------------------------

        # Move to next page, select options for region and data type here:
        set_statistic_type()
        # ---------------------------------------------------------------------

        # Move to next page, set start and end dates for dataset here:
        set_dates(timechunk[0], timechunk[1])
        # ---------------------------------------------------------------------

        # Move to next page, select options for data collection sites here:
        set_sites()
        # ---------------------------------------------------------------------

        # Move to confirmation page, enter email address to receive data:
        enter_email = driver.find_element_by_name("f_email")
        enter_email.send_keys("corinne.bosley@metoffice.gov.uk")

        get_data = driver.find_element_by_name("go")
        get_data.click()

        # confirmation = driver.get_screenshot_as_png()
        # confirmation.save("confirmations/download_confirmation_" +
        #                   key + timechunk[0] + timechunk[1] + ".png")


# TODO: Add printout of confirmation page somehow
# TODO: swap my email address for Elle"s

# driver.quit()
