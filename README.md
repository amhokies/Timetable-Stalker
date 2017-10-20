# Timetable-Stalker
A python application to stalk the Virginia Tech course time table

## Requirements
- At least Python 3.4 (comes with pip)

## Setup

1. Create a [Pushbullet](https://www.pushbullet.com/) account and follow their instructions for setting up push notifications on the devices that you want to receive notifications.

2. Create your Pushbullet access token by going to your Pushbullet [account settings](https://www.pushbullet.com/#settings/account)
![Generating your Pushbullet access token](http://i.imgur.com/veHK8UI.png "Generating your Pushbullet access token")

3. Enter your access token into the `pb_token` configuration option in config.yml.

4. Enter the term/year you want to search in config.yml.

5. Install dependencies with `pip3 install -r requirements.txt; pip3 install -r optional.txt`

## Usage

### Monitoring a specific course section by CRN

Usage: `python3 app.py crn COURSE_REQUEST_NUMBER`

Example: `python3 app.py crn 18143`

### Monitoring all sections of a course

Usage: `python3 app.py course "SUBJ_AND_NUM"`

Example: `python3 app.py course "MATH 2214"`

### Command Line Flags

    usage: app.py [-h] [-p] [-d] [-f CONFIG] [-o] {crn,course} search_term
    
    positional arguments:
      {crn,course}          Whether to monitor a course by crn or by the course
                            subject and number
      search_term           The crn or course subject and number. If using the
                            course subject and number, they must be enclosed in
                            quotation marks. For instance: "MATH 2214"
    
    optional arguments:
      -h, --help            show this help message and exit
      -p, --pushbullet      Send notification with pushbullet
      -d, --desktop         Send alert via libnotify
      -f CONFIG, --config CONFIG
                            Specify alternative config file
      -o, --oneshot         Check just once, then exit
    
