from FacialRecog import FacialRecog
from Guide import Guide
from Bot import Bot


def main():
    bot.display(guest_info)
    guide.find_face()
    bot.say('please follow me')
    bot.inform_host('hi@hi.hi')
    guide.guide_route()


if __name__ == '__main__':
    facial_data = None
    guest_info = {}
    host = ''
    port = 0
    password = ''
    bot = Bot(host, port, password)
    face = FacialRecog(facial_data)
    guide = Guide(face, guest_info, bot)
    main()
