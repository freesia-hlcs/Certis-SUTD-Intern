from FacialRecog import FacialRecog
from Guide import Guide
from Bot import Bot
from Kiosk import Kiosk
import cv2


def main():
    bot.display(guest_info)
    guide.find_face()
    bot.say('please follow me')
    bot.inform_host('hi@hi.hi')
    guide.guide_route()


if __name__ == '__main__':
    kiosk = Kiosk()
    guest_info = kiosk.get_guest_info()
    host = ''
    port = 0
    password = ''
    bot = Bot(host, port, password)
    face = FacialRecog()
    face.add_new('Michael', cv2.imread('michael2.jpg'))
    guide = Guide(face, guest_info, bot)
    main()
