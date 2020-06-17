"""
Container for processes repeated over various download scripts.

"""
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select


driver = webdriver.Firefox()

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

