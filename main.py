from FacialRecog import FacialRecog
from Bot import Bot
from Lift import Lift
from Kiosk import Kiosk
from Speech import *
import cv2
from time import sleep
import threading


def get_guest_info():
    global facial_recog
    global kiosk
    print('Getting guest info')
    name, venue = kiosk.get_guest_info()
    face_pic = kiosk.get_guest_pic()
    guest_info = {'name': name,
                  'venue': venue,
                  'face': facial_recog.get_face(face_pic)[0]}
    return guest_info


def wait_til(check_method, args=None, reference_value=True):
    while not check_method(args) == reference_value:
        sleep(0.1)
    return True


def eyes():
    global facial_recog
    global faces
    global bot_state
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        faces = facial_recog.main(frame)
        cv2.imshow('window', frame)
        sleep(0.2)
        if bot_state == 'idle':
            break
    video_capture.release()
    cv2.destroyAllWindows()


def approach_guest(guest_name):
    global bot
    global facial_recog
    global faces
    current_location = bot.get_current_location()
    reached = False
    state = 'patrolling'
    bot.patrol(current_location)
    while not reached:
        if state == 'approaching':
            if guest_name in faces:
                r = faces[guest_name]['r']
                th = faces[guest_name]['th']
                point = bot.get_point(r, th)
                print(point)
                bot.go_to_point(point)
                reached = r < 100
            elif bot.check_reached():
                bot.stop()
                bot.patrol(current_location)
                reached = False
                state = 'patrolling'
        else:
            if guest_name in faces:
                r = faces[guest_name]['r']
                th = faces[guest_name]['th']
                point = bot.get_point(r, th)
                bot.stop()
                bot.go_to_point(point)
                reached = r < 100
                state = 'approaching'
        sleep(0.2)
    bot.stop()


def guide(name, destination):
    global bot
    global faces
    bot.go_to_goal(destination)
    reached = bot.check_reached()
    while not reached:
        if name not in faces or faces[name]['r'] > 100:
            bot.stop()
            approach_guest(name)
            bot.go_to_goal(destination)
        reached = bot.check_reached()
        sleep(0.2)
    bot.stop()


def main():
    global facial_recog
    global bot
    global lift
    global bot_state
    say('Getting info from kiosk')
    guest_info = get_guest_info()
    name = guest_info['name']
    img = guest_info['pic']
    destination = guest_info['venue']
    facial_recog.train(name, img)
    say('Getting guest picture')
    approach_guest(name)
    say('Hello, %s! I will be your guide today!' % name)
    guide(name, 'lobby_lift')
    say('Calling lift')
    lift.call_lift(1)
    say('Opening lift door')
    lift.open_door()
    say('Please go in the lift!')
    lift.close_door()
    lift.go_to_level(destination[0])
    lift.open_door()
    bot.go_to_goal('outside lift')
    say('Please follow me')
    lift.close_door()
    guide(name, destination['venue'])
    bot_state = 'idle'


if __name__ == '__main__':
    bot = Bot('192.168.43.11', 7171, 'adept')
    kiosk = Kiosk()
    lift = Lift()
    facial_recog = FacialRecog()
    bot_state = 'idle'
    faces = {}
    while True:
        if bot_state == 'idle':
            text = input('Is the guest here?\n')
            if text == 'y':
                bot_state = 'guest'
        else:
            t_eyes = threading.Thread(target=eyes, args=())
            t_main = threading.Thread(target=main, args=())
            t_eyes.start()
            t_main.start()
            t_eyes.join()
            t_main.join()
            bot_state = 'idle'
            bot.go_to_goal('lobby')
