import socket
from time import sleep


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

    def go_to(self, goal_name):
        command = 'goto ' + goal_name
        return self.cmd(command)

    def go_to_level(self, level):
        command = 'localizeAtGoal ' + level
        return self.cmd(command)

    def check_reached(self, goal_name):
        return True

    def patrol(self, route_name):
        command = 'patrol ' + route_name
        return self.cmd(command)

    def say(self, to_say):
        command = 'say ' + to_say
        return self.cmd(command)

    def display(self, to_display):
        print('Displaying guest info: %s' % to_display)
        return True

    def wait_til(self, check_method, args=None, reference_value=True):
        while not check_method(args) == reference_value:
            sleep(0.1)
        return True

    def dock(self):
        command = 'dock'
        return self.cmd(command)

    def undock(self):
        command = 'undock'
        return self.cmd(command)

    def inform_host(self, host_email):
        print('Sending email')
        return True

    def get_status(self):
        print('Getting status')
        self.cmd('status')
        status_s = self.receive()
        status_s += self.receive()
        status_l = status_s.split('\r\n')
        # print(status_s)
        # print(status_l)
        status_d = {}
        for item in status_l:
            try:
                key, value = tuple(item.split(': '))
                status_d[key] = value
            except ValueError:
                pass
        return status_d


if __name__ == '__main__':
    import threading

    bot = Bot('192.168.43.11', 7171, 'adept')
    print(bot.get_status())


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
