# Timetable-Stalker
A python application to stalk the Virginia Tech course time table

## Setup

1. Create a [Pushbullet](https://www.pushbullet.com/) account and follow their instructions for setting up push notifications on the devices that you want to receive notifications.

2. Create your Pushbullet access token by going to your Pushbullet [account settings](https://www.pushbullet.com/#settings/account)
![Generating your Pushbullet access token](http://i.imgur.com/veHK8UI.png "Generating your Pushbullet access token")

3. Enter your access token into the pb_token configuration option in config.yml.

4. Install dependencies with `pip install -r requirements.txt`

## Usage

### Monitoring a specific course section by CRN

Usage: `python app.py crn COURSE_REQUEST_NUMBER`

Example: `python app.py crn 18143`

### Monitoring all sections of a course

Usage: `python app.py course "SUBJ_AND_NUM"`

Example: `python app.py course "MATH 2214"`


