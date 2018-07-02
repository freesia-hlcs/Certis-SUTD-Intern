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


def approach_guest(guest_info):
    global bot
    global facial_recog
    guest_name = guest_info['name']
    current_location = bot.get_current_location()
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    faces = facial_recog.main(frame)
    if guest_name in faces:
        found = True
        point = bot.get_point(faces[guest_name]['r'], faces[guest_name]['th'])
    else:
        found = False
        point = None
    if found:
        bot.go_to_point(point)
        state = 'approaching'
    else:
        bot.patrol(current_location)
        state = 'patrolling'
    reached = False
    while not reached:
        ret, frame = video_capture.read()
        faces = facial_recog.main(frame)
        if guest_name in faces:
            found = True
            r = faces[guest_name]['r']
            th = faces[guest_name]['th']
            point = bot.get_point(r, th)
            if r < 100:
                reached = True
                continue
        else:
            found = False
        if state == 'approaching':
            if found:
                bot.go_to_point(point)
            elif bot.check_reached():
                bot.patrol(current_location)
                state = 'patrolling'
        else:
            if found:
                bot.stop()
                bot.go_to_point(point)
                state = 'approaching'
        sleep(0.2)
    bot.stop()
    video_capture.release()


def guide(name, current_location, destination):
    global bot
    global facial_recog
    print('Guiding to %s' % destination)
    bot.patrol(current_location)
    video_capture = cv2.VideoCapture(0)
    reached = False
    state = 'face lost'
    i = 0
    while not reached:
        ret, frame = video_capture.read()
        if state == 'face lost':
            face = facial_recog.find_face(name, frame)
            if face:
                print('face found')
                state = 'face found'
                if i >= 5:
                    bot.stop()
                    bot.go_to(destination)
                    i = 0
            else:
                if i >= 5:
                    print('looking for guest')
                    bot.stop()
                    bot.patrol(current_location)
                else:
                    print('guest lost')
                    i += 1
        elif state == 'face found':
            face = facial_recog.find_face(name, frame)
            if not face:
                print('face lost')
                i = 0
                state = 'face lost'
            else:
                say('Please follow me')
                print('leading guest')
                # i += 1
                # if i > 5:
                #     reached = True
        sleep(0.2)
        reached = bot.check_reached()
    video_capture.release()


def main(guest_info):
    global bot
    global lift
    global activated
    global speech
    while not activated:
        sleep(0.5)
    name = guest_info['name']
    venue = guest_info['venue']
    face = guest_info['face']
    print('Guiding %s to %s' % (name, venue))
    sleep(1)
    bot.display(face)
    print('Displaying guest info')
    sleep(1)
    approach_guest(guest_info)
    print('Guest found')
    say('Hello, %s! I am your robot guide for today!' % name)
    sleep(1)
    print('Informing host that guest is currently on the way')
    sleep(1)
    guide(name, 'lobby', 'lobby lift')
    lift.call_lift(1)
    lift.open_door()
    print('Waiting for guest to go in')
    sleep(1)
    bot.go_to('lift_1')
    print('Going into lift')
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
    print('Going out of lift')
    sleep(1)
    guide(name, venue, venue)
    bot.stop()
    print('Reached goal')
    sleep(1)
    print('Informing host that guest has arrived')
    speech.order_drink()
    speech.common_talk()
    activated = False


def get_kiosk():
    global guest_info
    global activated
    # while True:
    #     guest_info = get_guest_info()
    #     if guest_info:
    #         activated = True
    guest = input('Is guest here? ')
    if guest == 'y':
        activated = True
    else:
        get_kiosk()


def convo():
    global speech
    speech.common_talk()
    pass


def send():
    global bot
    while True:
        to_send = input('Enter command:\n')
        print('Sending to bot: ' + to_send)
        bot.cmd(to_send)


if __name__ == '__main__':
    bot = Bot('192.168.43.11', 7171, 'adept')
    lift = Lift()
    kiosk = Kiosk()
    facial_recog = FacialRecog()
    speech = Speech()
    # guest_info = get_guest_info()
    guest_info = {'name': 'Michael',
                  'venue': {'name': 'EBC', 'level': 7},
                  'face': cv2.imread('michael2.jpg')}
    facial_recog.train(guest_info['name'], guest_info['face'])
    activated = False
    t_kiosk = threading.Thread(target=get_kiosk, args=())
    t_guide = threading.Thread(target=main, args=(guest_info,))
    t_speech = threading.Thread(target=convo, args=())
    t_send = threading.Thread(target=send, args=())
    t_kiosk.start()
    t_guide.start()
    t_speech.start()
    t_send.start()
    t_kiosk.join()
    t_guide.join()
    t_speech.join()
    t_send.join()
