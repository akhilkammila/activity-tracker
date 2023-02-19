# Include absolute path here if running a cron job

import requests
import collections
from config import TWILIO_SID, TWILIO_TOKEN, TWILIO_NUMBER, TARGET_NUMBER
from twilio.rest import Client
import datetime

def get_time_spent():
    # Get the time spent data, aggregate it in a dictionary
    x = requests.get('http://localhost:5600/api/0/export').json() #localhost5600 will work if ActivityWatch is downloaded
    aw_watcher_name = list(x['buckets'].keys())[0]
    events = x['buckets'][aw_watcher_name]['events']

    time_spent = collections.defaultdict(int)
    titles_times = collections.defaultdict(int)
    total = 0
    for index, event in enumerate(events):
        app = event['data']['app']
        title = event['data']['title']
        duration = event['duration']
        time_spent[app] += duration
        titles_times[(app, title)] += duration
        total += duration
    
    # Find the top 5 contributors
    contributors = []
    precision = 1
    num_apps = 5
    for key, value in sorted(time_spent.items(), key=lambda pair:-pair[1]):
        if num_apps <= 0: break
        contributors.append([key, round(value/60, precision), round(value/total*100, precision)])
        num_apps -= 1

    # Include the top 5 titles
    titles = []
    num_titles = 3
    for key, value in sorted(titles_times.items(), key=lambda pair:-pair[1]):
        if num_titles <= 0: break
        titles.append([key, round(value/60, precision), round(value/total*100, precision)])
        num_titles -= 1

    send_text(contributors, titles, round(total/60, precision))

def send_text(contributors, titles, total):
    send_text = True

    # Prepare messages
    today = datetime.date.today()
    msg = f"You spent {total} minutes today: {today}."
    msg += '\nApps:'
    for app, minutes, percent in contributors:
        msg += (f'\n{app}: {minutes} minutes ({percent}%)')
    msg += '\nTitles:'
    for (app, title), minutes, percent in titles:
        msg += (f'\n{app} > {title}: {minutes} minutes ({percent}%)')
    print(msg)

    # Send message
    if send_text:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages \
            .create(
                    body=msg,
                    from_=TWILIO_NUMBER,
                    to=TARGET_NUMBER)

get_time_spent()