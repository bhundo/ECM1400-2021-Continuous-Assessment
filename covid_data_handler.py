"""Handler of any forms of covid data used within the main.py module, 
    examples: total deaths, hospital cases"""
import logging
import sched
import time
import json  # pip install sched, pip install json
from uk_covid19 import Cov19API  # pip install uk_covid19

logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG)

def parse_csv_data(csv_filename):
    """Reads the csv file and returns the data from the csv as an array of lists."""
    data = []
    with open(csv_filename, "r", encoding='utf-8') as csv_file:
        for line in csv_file:
            data.append(line)
    return data
# parse_csv_data('nation_2021-10-28.csv')


def process_covid_csv_data(covid_csv_data):
    """Processes the covid data from the csv file in order to 
        return the cases in the last 7 days, the current hospital cases 
        and the total deaths."""
    new_cases_by_date = []
    hospital_cases = []
    cum_daily_deaths_by_date = []
    last7days_cases = 0
    for line in covid_csv_data:
        data = line.strip()
        data_array = data.split(",")
        new_cases_by_date.append(data_array[6])
        hospital_cases.append(data_array[5])
        cum_daily_deaths_by_date.append(data_array[4])
    for line in new_cases_by_date[3:10]:
        if isinstance(line, str):
            last7days_cases += int(line)
    current_hospital_cases = int(hospital_cases[1])
    total_deaths = int(cum_daily_deaths_by_date[14])
    return last7days_cases, current_hospital_cases, total_deaths

# process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))

def covid_API_request(location=json.loads(open("config.json", encoding='utf-8').read())["location"], 
    location_type=json.loads(open("config.json", encoding='utf-8').read())["location_type"]):
    """(Based on the location and location_type specified within the config file).
    Loads the covid data from the Cov19API module, 
    this is then processed using the 'filters' and 'structure' 
    variables and the 'data' key within the dictionary identifies 
    the portion of the dictionary that is wanted from this function."""
    filters = ['areaType=' + location_type, 'areaName=' + location]
    structure = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
        "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate"}
    api = Cov19API(filters=filters, structure=structure)
    covidapi_dict = api.get_json()
    logging.info("covid_API_request has been called successfully")
    return covidapi_dict


def nationalcoviddata(nation=json.loads(open("config.json", encoding='utf-8').read())["nation"]):
    """Similar to the covid_API_request function, 
    however instead of collecting local data, this function will 
    return national data for the nation specified within the config file."""
    filters = ['areaType=nation', 'areaName=' + nation]
    structure = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate",
        "hospitalCases": "hospitalCases",
        "newCasesByPublishDate": "newCasesByPublishDate"}
    api = Cov19API(filters=filters, structure=structure)
    nationcovidapi_dict = api.get_json()
    logging.debug("nationalcoviddata function has been called successfully")
    return nationcovidapi_dict

# nationalcoviddata()

def update_covid():
    covid_API_request()

def schedule_covid_updates(update_interval, update_name, repeat=False, cancelled=False):
    """Schedules updates for the covid data based upon the inputs in the website template.
    'update_interval' - time in seconds before the update commences
    'update_name' - the name of the update
    'repeat' - True = covid update will repeat"""
    logging.basicConfig(filename="log.log")
    covidscheduler = sched.scheduler(time.time, time.sleep)
    e1 = covidscheduler.enter(update_interval, 1, update_covid)
    if repeat is True:
        e2 = covidscheduler.enter(update_interval, 2, lambda: 
        schedule_covid_updates(update_interval=update_interval*24*60*60, update_name=update_name+' repeat', repeat=repeat))
    e3 = covidscheduler.enter(update_interval, 3, logging.info("scheduled covid data event completed"))
    if cancelled is True:
        covidscheduler.cancel(e1)
        covidscheduler.cancel(e2)
        covidscheduler.cancel(e3)
    covidscheduler.run(blocking=False)

#schedule_covid_updates(3, 'ben')
