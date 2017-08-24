#!/usr/bin/env python3

from datetime import datetime
import argparse
import course_search
import sys
import yaml
import time


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('search_type', choices=['crn', 'course'],
                        help='Whether to monitor a course by crn or by the course subject and number')
    parser.add_argument('search_term',
                        help="""The crn or course subject and number.
                                If using the course subject and number, they must be enclosed in quotation marks.
                                For instance: \"MATH 2214\" """)
    parser.add_argument('-p', '--pushbullet', action='store_true', help='Send notification with pushbullet')
    parser.add_argument('-d', '--desktop', action='store_true', help='Send alert via libnotify')
    parser.add_argument('-f', '--config', help='Specify alternative config file')
    parser.add_argument('-o', '--oneshot', action='store_true', help='Check just once, then exit')
    args = parser.parse_args()

    search_type = args.search_type
    search_term = args.search_term
    search_term_split = search_term.split()

    oneshot = args.oneshot
    use_pushbullet = args.pushbullet
    use_libnotify = args.desktop

    # Check that if the search type is "course", the search term is two words (the subject and course number)
    if search_type == 'course' and not len(search_term_split) == 2:
        print('When using the course search type, the search term must be two words (the course subject and number', file=sys.stderr)
        exit(1)

    # Thanks to Ethan Gaebel for this term information
    terms = {
        "winter" : "12",
        "spring" : "01",
        "summer i" : "06",
        "summer ii" : "07",
        "fall" : "09"
    }

    config = None
    config_path = None
    if args.config is not None:
        config_path = args.config
    else:
        config_path = 'config.yml'

    try: 
        with open(config_path, 'r') as config_file:
            try:
                config = yaml.load(config_file)
            except yaml.YAMLError as err:
                print(err,file=sys.stderr)
                exit(1)
    except FileNotFoundError as err:
        print('No such config file', file=sys.stderr)
        exit(1)
    
    if config is None:
        print('Error with your config', file=sys.stderr)
        exit(1)
    elif use_pushbullet == True and 'pb_token' not in config:
        print('Config must contain your Pushbullet Access Token!', file=sys.stderr)
        exit(1)
    elif ('term' not in config) or (config['term'] not in terms):
        print('No term (or an incorrect term) specified in config!', file=sys.stderr)
        exit(1)
    elif 'year' not in config:
        print('Year not specified in config!', file=sys.stderr)
        exit(1)

    if use_pushbullet == True:
        from pushbullet import Pushbullet
        pb = Pushbullet(config['pb_token'])

    if use_libnotify == True:
        import notify2
        notify2.init("Timetable-Stalker")


    semester = str(config['year'])+terms.get(config['term'])

    last_open_courses = list()

    while True:
        print("Starting check... ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file=sys.stderr)

        if search_type == 'crn':
            courses = course_search.get_open_courses_by_crn(search_term, semester)
        else:
            subj = search_term_split[0]
            num = search_term_split[1]

            courses = course_search.get_open_courses_by_course(subj, num, semester)

        # Get only courses that have opened up since the last check
        new_open_courses = list(set(courses) - set(last_open_courses))
        last_open_courses = courses

        if len(new_open_courses) == 0:
            print("No new courses found!!!")
        else:
            first_course = new_open_courses[0]

            title = "{} is open!".format(first_course.label)

            if len(new_open_courses) == 1:
                message = "{} is open!".format(repr(first_course))
            else:
                message = "{} and {} others are open!".format(repr(first_course), len(new_open_courses) - 1)

            if use_pushbullet == True:
                pb.push_note(title, message)

            if use_libnotify == True:
                notify2.Notification(title, message, "emblem-important").show()

            print(message)
            if oneshot == True:
                exit(0)

        time.sleep(30)
