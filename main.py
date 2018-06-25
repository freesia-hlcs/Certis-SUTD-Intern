from FacialRecog import FacialRecog
# from Guide import Guide
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


def guide(guest_info):
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
    for i in range(10):
    # while not found:
        ret, frame = video_capture.read()
        found = facial_recog.find_face(name, frame)
        sleep(0.2)
    # bot.stop()
    video_capture.release()
    print('Guest found')
    # bot.go_to('lobby_lift')
    print('Going to lobby lift')
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
    reached = False
    for i in range(10):
    # while not reached:
    #     reached = bot.check_reached(venue)
        sleep(0.2)
    # bot.stop()
    print('Reached goal')


if __name__ == '__main__':
    bot = Bot('192.168.0.250', 7171, 'adept')
    lift = Lift()
    kiosk = Kiosk()
    facial_recog = FacialRecog()
    guest_info = {
        'name': 'Michael',
        'venue': {'name': 'EBC', 'level': 7},
        'face': cv2.imread('michael2.jpg')
    }
    facial_recog.add_face(guest_info['name'], guest_info['face'])
    guide(guest_info)
