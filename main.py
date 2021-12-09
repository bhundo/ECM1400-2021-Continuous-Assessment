"""The main source code for the Flask website, run this code and enter 
'localhost:5000/index' in order to view the template"""
import datetime
import logging
from flask import Flask, render_template, request
from covid_data_handler import *
from covid_news_handling import *
logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG)

# request.args =
# http://localhost:5000/index?update=00%3A15&two=Ben&repeat=repeat&covid-data=covid-data&news=news#

# create app
app = Flask("__name__")
updates = []
nationaldata = nationalcoviddata()
coviddata = covid_API_request()

# create index route and render intial template
newCasesByPublishDate = []
for line in coviddata['data']:
    newCasesByPublishDate.append(line["newCasesByPublishDate"])
local7dayscases = sum(newCasesByPublishDate[0:8])
newCasesByPublishDate = []
for line in nationaldata['data']:
    newCasesByPublishDate.append(line["newCasesByPublishDate"])
nation7dayscases = sum(newCasesByPublishDate[0:8])
hospitalCases = []
for line in nationaldata['data']:
    hospitalCases.append(line["hospitalCases"])
current_hospital_cases = hospitalCases[0]
cumDeaths28DaysByDeathDate = []
for line in nationaldata['data']:
    cumDeaths28DaysByDeathDate.append(line["cumDeaths28DaysByDeathDate"])
total_deaths = int(cumDeaths28DaysByDeathDate[1])


def remove_completed_update():
    """function is used if the scheduled event is complete, 
        or if the user has deleted an event from the scheduler"""
    title = request.args["update_item"]
    for update in updates:
        if update["title"] == title:
            updates.remove(update)


@app.route("/index")
def template():
    """Defines the template and returns the rendered version of the template
    with the inputs that the user has given, once run the software needs
    the url 'localhost:5000/index' to be loaded in a web browser in order to view the template"""
    # if a news article is removed

    # if the submit button is used, converting alarm time to clock time
    # and coverting to seconds for the scheduler#
    if "two" in request.args:
        clock_time = datetime.datetime.now()
        alarm_time = request.args["update"].split(":")
        update_time = clock_time.replace(
            hour=int(alarm_time[0]), minute=int(alarm_time[1]))

        if clock_time > update_time:
            update_time = update_time + datetime.timedelta(days=1)

        update_in_seconds = int((update_time - clock_time).total_seconds())
        repeat_update = False
        print(update_in_seconds)
        # if repeat is included in the index url then set repeat to True
        if "repeat" in request.args:
            repeat_update = True
            repeat_content = "repeat has been triggered"
            repeat_updates = {"title": "", "content": repeat_content}
            updates.append(repeat_updates)

        # using the 'update news' and 'update covid data' buttons and catching from the url
        if "covid-data" in request.args:
            covid_data_content = (
                "update at: " + request.args["update"] + " for covid data."
            )
            covid_data_title = "Covid Data Update: " + request.args["two"]
            covid_updates = {"title": covid_data_title,
                             "content": covid_data_content}
            updates.append(covid_updates)
            schedule_covid_updates(
                update_in_seconds, (request.args["two"]), repeat_update)

        if "news" in request.args:
            content = "update at: " + request.args["update"] + " for news."
            news_title = "News Update: " + request.args["two"]
            news_updates = {"title": news_title, "content": content}
            updates.append(news_updates)
            schedule_news_updates(
                update_in_seconds, (request.args["two"]), repeat_update)

    if "update_item" in request.args:
        remove_completed_update()
        if "Covid+Data+Update" in request.args.get("update_item"):
            schedule_covid_updates(1, request.args.get(
                "update_item"), cancelled=True)
        if "News+Update" in request.args.get("update_item"):
            schedule_news_updates(1, request.args.get(
                "update_item"), cancelled=True)

    if "notif" in request.args:
        remove_news_article(request.args["notif"])
        logging.debug("News Article has been removed")

    return render_template(
        "index.html",
        title="Coronavirus Dashboard",
        location="Exeter",
        local_7day_infections=local7dayscases,
        deaths_total=total_deaths,
        hospital_cases=current_hospital_cases,
        nation_location="England",
        national_7day_infections=nation7dayscases,
        news_articles=news_articles[0:4],
        updates=updates,
        image="covid19.png",
    )


if __name__ == "__main__":
    app.run()
