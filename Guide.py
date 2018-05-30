from time import sleep


class Guide(object):

    def __init__(self, face, guest_info, bot):
        # face is a FacialRecog object
        # guest_info is a dictionary
        # bot is a Bot object
        self.state = 'standby'
        self.face = face
        self.guest_name = guest_info['name']
        self.destination = guest_info['destination']
        self.scheduled_time = guest_info['scheduled_time']
        self.host = guest_info['host']
        self.bot = bot

    def operate_lift(self, from_level, to_level):
        if from_level == to_level:
            pass
        else:
            self.bot.call_lift(from_level)
            self.bot.say('please go in')
            self.bot.wait_til('guests are in')
            self.bot.go_in_lift()
            self.bot.press_lift(to_level)
            self.bot.go_out_lift()
            self.bot.say('please follow me')

    def check_face(self):
        check = self.face.get_face()
        distance = self.face.get_distance()
        max_distance = 10
        return check and distance <= max_distance

    def go_to_destination(self, destination):
        self.bot.go_to(destination)

    def is_reached(self):
        reached = self.bot.check_reached(self.destination)
        return reached

    def guide(self, destination):
        reached = False
        while not reached:
            if self.check_face():
                self.go_to_destination(destination)
                sleep(1)
            else:
                buffer_time = 0
                while not self.check_face() and buffer_time < 10:
                    self.go_to_destination(destination)
                    sleep(1)
                    buffer_time += 1
                else:
                    if self.check_face():
                        self.go_to_destination(destination)
                        sleep(1)
                    else:
                        self.bot.stop()
                        self.find_face()
            reached = self.is_reached()

    def find_face(self):
        found = False
        while not found:
            self.bot.patrol()
            sleep(1)
            found = self.face.get_face()
        return found

    def guide_route(self):
        if self.destination.level == 1:
            self.guide(self.destination)
        else:
            lift_destination = None
            self.guide(lift_destination)
            self.operate_lift(1, self.destination.level)
            self.guide(self.destination)
