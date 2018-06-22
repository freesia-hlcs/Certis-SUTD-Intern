from FacialRecog import *
# from Guide import Guide
from Bot import Bot
from Lift import Lift
from Kiosk import Kiosk
import cv2
from time import sleep
import threading


def get_guest_info(kiosk):
    print('Getting guest info')
    name, venue = kiosk.get_guest_info()
    face_pic = kiosk.get_guest_pic()
    guest_info = {
        'name': name,
        'venue': venue,
        'face': getFace(face_pic)[0]
    }
    return guest_info


def guide(guest_info):
    global bot
    global lift
    name = guest_info['name']
    venue = guest_info['venue']
    face = guest_info['face']
    print('Guiding %s to %s' % (name, venue))
    bot.display(face)
    found = False
    video_capture = cv2.VideoCapture(0)
    bot.patrol('lobby')
    while not found:
        ret, frame = video_capture.read()
        found = find_face(face, frame)
        sleep(0.2)
    bot.stop()
    video_capture.release()
    print('Guest found')
    bot.go_to('lobby_lift')
    lift.call_lift(1)
    lift.open_door()
    print('Waiting for guest to go in')
    bot.go_to('lift_1')
    sleep(5)
    lift.close_door()
    lift.go_to_level(venue['level'])
    bot.go_to_level(venue['level'])
    lift.open_door()
    print('Waiting for guest to go out')
    sleep(5)
    lift.close_door()
    bot.go_to('venue_lift')
    bot.go_to(venue['room'])
    print('Going to %s' % venue)
    reached = False
    while not reached:
        reached = bot.check_reached(venue)
        sleep(0.2)
    bot.stop()
    print('Reached goal')


if __name__ == '__main__':
    bot = Bot('192.168.0.250', 7171, 'adept')
    lift = Lift()
    kiosk = Kiosk()
