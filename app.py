from datetime import datetime
from pushbullet import Pushbullet
import argparse
import course_search
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
    args = parser.parse_args()

    search_type = args.search_type
    search_term = args.search_term
    search_term_split = search_term.split()

    # Check that if the search type is "course", the search term is two words (the subject and course number)
    if search_type == 'course' and not len(search_term_split) == 2:
        print('When using the course search type, the search term must be two words (the course subject and number')
        exit(1)

    config = None

    with open('config.yml', 'r') as config_file:
        try:
            config = yaml.load(config_file)
        except yaml.YAMLError as err:
            print(err)
            exit(1)

    if config is None:
        print('Error with your config')
        exit(1)
    elif 'pb_token' not in config:
        print('Config must contain your Pushbullet Access Token!')
        exit(1)

    pb = Pushbullet(config['pb_token'])

    last_open_courses = list()

    while True:
        print("Starting check... ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        if search_type == 'crn':
            courses = course_search.get_open_courses_by_crn(search_term)
        else:
            subj = search_term_split[0]
            num = search_term_split[1]

            courses = course_search.get_open_courses_by_course(subj, num)

        # Get only courses that have opened up since the last check
        new_open_courses = list(set(courses) - set(last_open_courses))
        last_open_courses = courses

        if len(new_open_courses) == 0:
            print("No new courses found!!!")
        else:
            first_course = new_open_courses[0]

            title = "{} is open!".format(first_course.label)

            if len(courses) == 1:
                message = "{} is open!".format(repr(first_course))
            else:
                message = "{} and {} others are open!".format(repr(first_course), len(new_open_courses) - 1)

            pb.push_note(title, message)

            print(message)

        time.sleep(30)
