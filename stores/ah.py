import argparse
import datetime
import re
import time
import copy
import locale
import logging
from notification import twilio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.option import Options

def find_slot(driver,notificationclient, postcode, min_date, max_date):

    driver.get("https://www.ah.nl/kies-moment/bezorgen/" + postcode)

    #Accept the cookie prompt if it pops up
    try:
        cookie_monster = driver.find_element(By.ID, 'accept-cookie')
        cookie_monster.click()
    except NoSuchElementException as e:
        # No Cookies here
        pass

    ############## Find a delivery slot for the postcode ###########

    found_slot = False
    datelist = []

    while True:

        tempdatelist = driver.find_elements(By.CSS_SELECTOR, '.delivery-date-selector__timespan .delivery-date-selector__day')

        if  datelist !=tempdatelist:
            datelist = tempdatelist
        else:
            logging.info("This is some random infinite loop")
            return

        for datebtn in datelist:
            if "-disabled" not in datebtn.get_attribute("class"):
                time.sleep(2)
                datebtn.click()
                time.sleep(2)
                try:
                    saved = locale.setlocale(locale.LC_ALL)
                    locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')
                    searching_date = datetime.datetime.strptime(re.findall("[0-9]+ [a-z]{3}", datebtn.text)[0], "%d %b")
                    locale.setlocale(locale.LC_ALL, saved)
                except ValueError as e:
                    logging.info("Cant parse this date : {} ".format(datebtn.text))
                    continue

                #Include min date
                #logging.info("{} <= {} : {}".format(searching_date, min_date, seaching_date <= min_date))
                if searching_date < min_date or searching_date > max_date:
                    logging.info("This is not the date you are searching for : {}".format(datebtn.text))
                    continue

                time.sleep(2)
                timelist = driver.find_elements(By.CSS_SELECTOR, '.delivery-time-selector__container .delivery-time-selector__table .timeslot-block')

                for timeslot in timelist:
                    if "timeslot-block--disabled" not in timeslot.get_attribute("class"):
                        logging.info("Found a date and a time slot : {} {}".format(searching_date, timeslot.text))
                        found_slot = True 
                        break
                
            if found_slot:
                # Doby is a free elf
                break
        if found_slot:
            # Doby is a free elf
            break


        try:
            nextbtn = driver.find_element(By.CSS_SELECTOR,'.delivery-date-selector__next')
            if nextbtn.is_displayed() and nextbtn.is_enabled():
                logging.info("Going to next page")
                time.sleep(2)
                nextbtn.click()
                time.sleep(2)
            else:
                break
        expect NoSuchElementException as e:
            print(e)
            break

        if found_slot:
            notificationclient.notify_me("Founf empty delivery slot")
            return

        logging.info("Not a single slot is available.")
        return

    
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--postcode', type=str, required=True)
        parser.add_argument('--min_date', type=str, default=None)
        parser.add_argument('--max_date', type=str, default=None)
        parser.add_argument('--background', action='store_true')
        parser.add_argument('--twilio_sid', type=str, required=True)
        parser.add_argument('--twiliio_token', type=str, required=True)
        parser.add_argument('--my_number', type=str, required=True)
        parser.add_argument('--twilio_number', type=str, default='')
        parser.add_argument('--log-level', choices=['info', 'warning', 'error'], default='warning')

        args = parser.parse_args()

        return args


    def main():
        args = parse_args()

        logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))

        notificationclient = twilio.Notification( args.twilio_sid, args.twiliio_token, args.my_number, args.twilio_number )

        chrome_options = Options()
        if args.background:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument("--disable-extensions"); # disabling extensions
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu"); # applicable to windows os only
        chrome_options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
        chrome_options.add_argument("--no-sandbox"); # Bypass OS security model

        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.implicitly_wait(60) # seconds

        min_date = args.min_date
        if min_date is not None:
            min_date = datetime.datetime.strptime(min_date, "%d %b")

        max_date = args.max_date
        if max_date is not None:
            max_date = datetime.datetime.strptime(max_date, "%d %b")

        find_slot(driver, notificationclient, args.postcode, min_date, max_date)

        driver.close()
