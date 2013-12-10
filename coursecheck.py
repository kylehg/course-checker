import time

from twilio.rest import TwilioRestClient

from config import API_PW, API_UN, TWILIO_SID, TWILIO_TOKEN
from registrar import Registrar

COURSES = (
    ('hist', '212', '302'), # Utopia
    ('fnar', '637', '401'), # Info viz
    ('cine', '116', '403'), # Screenwriting workshop
    ('psci', '395', '301'), # Power sharing
    ('lasf', '302', '131'),
)

RATE_LIMIT_PER_HOUR = 1000

def alert(section):
    print 'ALERT ALERT ALERT', section
    pass

def check_courses(r, courses):
    print 'Checking %d courses' % len(courses)
    for course in courses:
        try:
            sect = r.section(*course)
        except Exception, e:
            print '[%s-%s-%s] ERROR: %s' % (course[0], course[1], course[2], e)
            continue

        if sect['is_closed']:
            print '[%s] CLOSED %s' % (sect['section_id_normalized'], sect['course_title'])
        else:
            print '[%s] %s %s' % (sect['section_id_normalized'],
                                  sect['course_status_normalized'].upper(),
                                  sect['course_title'])
            alert(sect)



if __name__ == '__main__':
    r = Registrar(API_UN, API_PW)
    while True:
        check_courses(r, COURSES)
        seconds_to_sleep = (60 * 60) / (RATE_LIMIT_PER_HOUR / len(COURSES))
        time.sleep(seconds_to_sleep)
