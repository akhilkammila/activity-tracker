# Activity Tracker

## About

Activity Tracker is a python script built on the open source project ActivityWatch. We parse through ActivityWatch's event data to retrieve the most used apps and app titles. We then text users with detailed information on their computer activity.

## Instructions for use

1. Clone Activity Tracker's github repository and install dependencies.
2. Install Activity Watch (https://activitywatch.net/)
3. Create a config.py file, and fill with the following variables from your personal Twilio account: TWILIO_SID, TWILIO_TOKEN, TWILIO_NUMBER, TARGET_NUMBER.
4. Run activitytracker.py. Uncomment scheduler code or run a cron job to receive texts daily.

## Upcoming Changes

We hope to integrate with AWS lambda and create a web app so that users do not have to run scripts or cron jobs locally.
