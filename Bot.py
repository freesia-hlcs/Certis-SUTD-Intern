import socket
from time import sleep
from math import cos, sin


class Bot(object):

    def __init__(self, host, port, password):
        print('connecting to bot')
        try:
            self.s = socket.socket()
            self.s.connect((host, port))
            password += '\r\n'
            password_b = password.encode('utf8')
            self.s.send(password_b)
            print('connected to the bot')
            text = ''
            while 'End of commands' not in text:
                text = self.receive()
                print(text)
        except socket.error as e:
            print(e)

    def receive(self, buffer_size=4096):
        msg_b = self.s.recv(buffer_size)
        msg = msg_b.decode('utf8')
        return msg

    def cmd(self, text):
        if text:
            text += '\r\n'
        text_b = text.encode('utf8')
        try:
            self.s.send(text_b)
            return True
        except socket.error as e:
            print(e)
            return False

    def stop(self):
        command = 'stop'
        return self.cmd(command)

    def go_to_goal(self, goal_name):
        command = 'goto ' + goal_name
        return self.cmd(command)

    def lift_to_level(self, level):
        command = 'localizeAtGoal %d_lift' % level
        return self.cmd(command)

    def check_reached(self, threshold=1):
        self.cmd('goalDistanceRemaining')
        distance = float(self.receive())
        if distance <= threshold:
            return True
        else:
            return False

    def patrol(self, route_name):
        command = 'patrol ' + route_name
        return self.cmd(command)

    def say(self, to_say):
        command = 'say ' + to_say
        return self.cmd(command)

    def display(self, to_display):
        print('Displaying guest info: %s' % to_display)
        return True

    def dock(self):
        command = 'dock'
        return self.cmd(command)

    def undock(self):
        command = 'undock'
        return self.cmd(command)

    def inform_host(self, host_email):
        print('Sending email to %s' % host_email)
        return True

    def get_status(self):
        print('Getting status')
        self.cmd('status')
        status_s = self.receive()
        status_s += self.receive()
        status_l = status_s.split('\r\n')
        status_d = {}
        for item in status_l:
            if not item.startswith('Status'):
                key, value = tuple(item.split(': '))
                status_d[key] = value
            else:
                status = item[8:].split(' ')
                s = {}
                for i in range(len(status)):
                    if status[i].endswith(':'):
                        try:
                            s[status[i][:-1]] = status[i+1]
                        except IndexError:
                            pass
                status_d['Status'] = s
        return status_d

    def get_bot_position(self):
        print('Getting bot position')
        location = self.get_status()['Location'].split(' ')
        position = (int(location[0]), int(location[1]), int(location[2]))
        return position

    def get_point(self, point_r, point_th):
        bot_x, bot_y, bot_th = self.get_bot_position()
        th = bot_th + point_th
        x = bot_x + point_r * cos(th)
        y = bot_y + point_r * sin(th)
        point = (x, y, th)
        return point

    def go_to_point(self, point):
        return self.cmd('goto %f %f %f' % point)

    def get_current_location(self):
        x, y, th = self.get_bot_position()
        return 'lobby'


if __name__ == '__main__':
    import threading

    bot = Bot('192.168.43.11', 7171, 'adept')


    def receive():
        while True:
            print(bot.receive())


    def send():
        while True:
            text = input('Enter command:\n')
            bot.cmd(text)


    t1 = threading.Thread(target=receive, args=())
    t2 = threading.Thread(target=send, args=())
    t1.start()
    t2.start()
    t1.join()
    t2.join()
