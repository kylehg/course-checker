import time

from penn.registrar import Registrar
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

from config import API_PW, API_UN, COURSES, PHONE_NUMBER, TWILIO_NUMBER, TWILIO_SID, TWILIO_TOKEN


RATE_LIMIT_PER_HOUR = 1000

r = Registrar(API_UN, API_PW)
client = TwilioRestClient(TWILIO_SID, TWILIO_TOKEN) if TWILIO_SID and TWILIO_TOKEN else None


def alert(sect):
    section_str = sect['section_id_normalized'] + ' ' + sect['course_title']
    print '!!! ALERT ALERT ALERT %s' % section_str
    if client is not None:
        body = '%s is now open!' % section_str
        try:
            message = client.sms.messages.create(body=body, to=PHONE_NUMBER, from_=TWILIO_NUMBER)
        except TwilioRestException, e:
            print 'TWILIO ERROR', e

def check_courses(courses):
    print 'Checking %d courses' % len(courses)
    for course in courses:
        try:
            sect = r.section(*course)
        except Exception, e:
            print '[%s-%s-%s] ERROR: %s' % (course[0], course[1], course[2], e)
            continue

        if sect['is_closed']:
            print '[%s] CLOSED %s' % (sect['section_id_normalized'], sect['course_title'])
            alert(sect)
        else:
            print '[%s] %s %s' % (sect['section_id_normalized'],
                                  sect['course_status_normalized'].upper(),
                                  sect['course_title'])
#            alert(sect)



if __name__ == '__main__':

    while True:
        check_courses(COURSES)
        seconds_to_sleep = (60 * 60) / (RATE_LIMIT_PER_HOUR / len(COURSES))
        time.sleep(seconds_to_sleep)
