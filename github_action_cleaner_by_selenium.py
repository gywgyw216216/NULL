#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import (sleep,
                  strftime, )
from sys import argv
from traceback import format_exc



# Define Global Variables. Change Values by Yourselves Except urls.
USERNAME = ''  # Your GitHub Username.
PASSWORD = ''  # Your GitHub Password.
REPOSITORY = ''  # GitHub Action's Repository Name.
URL_GITHUB = 'https://github.com/'  # Don't Change.
URL_GITHUB_LOGIN = URL_GITHUB + 'login/'  # Don't Change.
URL_GITHUB_ACTION = URL_GITHUB + USERNAME + '/' + REPOSITORY + '/actions/'  # Don't Change.
WORKFLOWS = 0  # Circles Number. (Workflows Number)



def print_traceback_error(exception: Exception):
    error = format_exc()
    error_time = strftime("%Y-%m-%d %H:%M:%S")
    command_line_entry = " ".join(argv)

    print(error_time + "\tERROR! ",
          end="")
    print(exception)
    print(command_line_entry + "\n" + error)
    print('--------------------------------------------------------')



def login_github(browser: webdriver):
    browser.find_element_by_name("login").send_keys(USERNAME)
    sleep(1)
    browser.find_element_by_name("password").send_keys(PASSWORD)
    sleep(1)
    browser.find_element_by_name("commit").send_keys(Keys.ENTER)  # Same as Line 43.
    # browser.find_element_by_name("commit").click()
    sleep(30)  # Input GitHub Verification Code Within 30 Seconds, or You Can Delete this Line.



def delete_actions(browser: webdriver,
                   number: int) -> bool:
    browser.find_element_by_class_name("timeline-comment-action.btn-link").click()
    sleep(1)
    browser.find_element_by_class_name("dropdown-item.btn-link.menu-item-danger ").click()
    sleep(1)

    try:
        browser.find_element_by_class_name("btn.btn-block.btn-danger").click()

        print("Delete " + str(number) + " Workflow Successfully! ")

        return True
    except Exception as exception:
        print_traceback_error(exception)

        return False



def main():
    browser = webdriver.Firefox()  # Default Browser Firefox. Put "geckodriver.exe" in Python's /Scripts Directory.
    browser.get(URL_GITHUB_LOGIN)
    login_github(browser)
    i = 0

    while i <= WORKFLOWS:
        browser.get(URL_GITHUB_ACTION)

        if delete_actions(browser,
                          WORKFLOWS - i):
            i += 1

    browser.close()
    browser.quit()



if __name__ == '__main__':
    main()
