# Groceries

It's tough to find delivery slots for groceries. This one is supposed to run as a cron which scans grocery stores (Albert Heijn for now) in your postcode (Netherlands) for free slots and gives you a call if there's an empty slot available in the schedule.


## Requirements

The setup requires Twilio account. If you have a paid one, good. If not, you can try this out with a trial account. You can verify your own number for free.

## Easy setup 

If you have docker installed on your system simply run this (ofcourse after replacing all the parameters)

```
docker run -i rajatsharma94/quarantine:groceries finddeliveryslot --postcode <postcode> --twilio_sid <twilio sid> --twilio_token <twilio auth token> --my_number "<phone number>" --min_date="<min_date>" --max_date="<max_date>" --log-level info --background
```

Example command would be something like : 

```
docker run -i rajatsharma94/quarantine:groceries finddeliveryslot --postcode 1234AB --twilio_sid my_twilio_sid --twilio_token my_twilio_token --my_number "+311234567" --min_date="16 apr" --max_date="15 may" --log-level info --background
```

## Script Setup (for looking under the hood)

- Register an account on Twilio. You can verify your own number for free
- This script requires python3 & pip3 installed
- Need to setup selenium driver for chrome. Download and install for your OS from here : https://chromedriver.chromium.org/downloads
- Install setuptools by running `pip3 install --upgrade setuptools`
- Run `cd groceries && python3 setup.py build && python3 setup.py install`

## Script Usage

Simply run (note the date needs to be in the mentioned format)

`finddeliveryslot --postcode <postcode> --twilio_sid <twilio sid> --twilio_token <twilio auth token> --my_number "<phone number>" --min_date="16 apr" --max_date="15 may"`

or for more options run 

`finddeliveryslot --help`
