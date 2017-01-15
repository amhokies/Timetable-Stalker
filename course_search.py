from bs4 import BeautifulSoup
from models.course import Course
import requests

default_postdata = {
    'CAMPUS': '0',
    'TERMYEAR': '201701',
    'CORE_CODE': 'AR%',
    'subj_code': '',
    'CRSE_NUMBER': '',
    'crn': '',
    'open_only': 'on',
    'BTN_PRESSED': 'FIND class sections',
}

url = 'https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest'


def _get_open_courses(data):
    req = requests.post(url, data=data)

    soup = BeautifulSoup(req.content, 'html5lib')

    rows = soup.select('table.dataentrytable tbody tr')

    open_courses = list()

    # The first row is the header row with the column labels
    # If there's only one row, the rest of the table is empty, so there are no results
    if len(rows) > 1:
        rows = rows[1:]

        for row in rows:
            cells = row.select('td')
            cells_text = list(map(lambda x: x.get_text(), cells))

            crn = cells_text[0].strip()
            label = cells_text[1].strip()
            title = cells_text[2].strip()
            professor = cells_text[6].strip()

            open_courses.append(Course(crn, label, title, professor))

    return open_courses


def get_open_courses_by_course(subj, num):
    """ Get the open courses that match the course subject and number passed in
    :param subj: The subject abbreviation
    :param num: The course number
    :return: Returns a list of the open courses that are matched
    """

    postdata = default_postdata.copy()

    postdata['subj_code'] = subj.strip().upper()
    postdata['CRSE_NUMBER'] = num.strip()

    return _get_open_courses(postdata)


def get_open_courses_by_crn(crn):
    """ Get the open course that matches the crn passed in
    :param crn: The course request number of the course section
    :return: Returns a list of the open courses that are matched
    """

    postdata = default_postdata.copy()

    postdata['crn'] = crn.strip()

    return _get_open_courses(postdata)
