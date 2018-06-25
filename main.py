from FacialRecog import FacialRecog
from Guide import Guide
from Bot import Bot
from Lift import Lift
from Kiosk import Kiosk
import cv2
from time import sleep
import threading


def get_guest_info(kiosk):
    global facial_recog
    print('Getting guest info')
    name, venue = kiosk.get_guest_info()
    face_pic = kiosk.get_guest_pic()
    guest_info = {
        'name': name,
        'venue': venue,
        'face': facial_recog.get_face(face_pic)[0]
    }
    return guest_info


def guide(name, current_position, destination):
    print('Guiding to %s' % destination)
    global bot
    global facial_recog
    # bot.go_to(destination)
    video_capture = cv2.VideoCapture(0)
    reached = False
    i = 0
    while not reached:
        ret, frame = video_capture.read()
        if not facial_recog.find_face(name, frame):
            i = 0
            print('guest lost')
            # bot.stop()
            # bot.patrol(current_position)
        else:
            print('leading guest')
            i += 1
            if i > 10:
                reached = True
            # bot.stop()
            # bot.go_to(destination)
            # reached = bot.check_reached(destination)
        sleep(0.2)
    video_capture.release()


def main(guest_info):
    global bot
    global lift
    name = guest_info['name']
    venue = guest_info['venue']
    face = guest_info['face']
    print('Guiding %s to %s' % (name, venue))
    # bot.display(face)
    print('Displaying guest info')
    found = False
    video_capture = cv2.VideoCapture(0)
    # bot.patrol('lobby')
    print('Patrolling lobby')
    # for i in range(10):
    while not found:
        print('Looking for face')
        ret, frame = video_capture.read()
        found = facial_recog.find_face(name, frame)
        sleep(0.2)
    # bot.stop()
    video_capture.release()
    print('Guest found')
    print('Informing host that guest is currently on the way')
    guide(name, 'lobby', 'lobby lift')
    lift.call_lift(1)
    lift.open_door()
    print('Waiting for guest to go in')
    # bot.go_to('lift_1')
    print('Going into lift')
    sleep(5)
    lift.close_door()
    lift.go_to_level(venue['level'])
    # bot.go_to_level(venue['level'])
    lift.open_door()
    print('Waiting for guest to go out')
    sleep(5)
    lift.close_door()
    # bot.go_to('venue_lift')
    # bot.go_to(venue['room'])
    print('Going out of lift')
    print('Going to %s' % venue)
    guide(name, venue, venue)
    # bot.stop()
    print('Reached goal')
    print('Informing host that guest has arrived')


if __name__ == '__main__':
    # bot = Bot('192.168.0.250', 7171, 'adept')
    print('connecting to bot')
    lift = Lift()
    kiosk = Kiosk()
    facial_recog = FacialRecog()
    guest_info = {
        'name': 'Michael',
        'venue': {'name': 'EBC', 'level': 7},
        'face': cv2.imread('michael2.jpg')
    }
    facial_recog.add_face(guest_info['name'], guest_info['face'])
    main(guest_info)
