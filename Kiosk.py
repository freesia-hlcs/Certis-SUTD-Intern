import time
import socket
import json
import os
from Naked.toolshed.shell import execute_js
import threading
from time import sleep

class Kiosk(object):

    def __init__(self):
        self.path = os.getcwd().replace('\\', '/')
        self.record_file = os.getcwd()+'/kiosk-pc-robot/'+'record.txt'
        self.file_path = os.getcwd() + '/kiosk-pc-robot/'+'/files/'
        self.node_path = os.getcwd() + '/kiosk-pc-robot/'+ 'server_final.js'
        self.json_list = [i for i in os.listdir(self.file_path) if i.endswith('.json')]
        self.pic_list = [i for i in os.listdir(self.file_path) if i.endswith('.png')]

    def insert_tolist(self, new_json):
        fp = open(self.record_file)
        fp = fp.readlines()
        lines = []
        for line in fp:
            lines.append(line)
        lines.insert(0, new_json + '\n')  # Insert the new file's name in at the first line.
        s = ''.join(lines)
        with open(self.record_file, 'w') as fp:
            fp.write(s)
            fp.close()

    def list_update(self):
        self.json_list = [i for i in os.listdir(self.file_path) if i.endswith('.json')]
        self.pic_list = [i for i in os.listdir(self.file_path) if i.endswith('.png')]


    def parse_json(self, file):
        f = open(self.file_path + file, encoding='utf-8')
        # Set encoding mode. This parameter needs to be utf-8 or the default mode will be gbk
        content = json.load(f)
        name, venue = content['visitor_name'], content['meeting_venue']
        picture = self.file_path + file.strip('.json') + '.png'
        # if picture not in pic_list:
        #     print("ERROR:The picture {} is not stored".format(picture))
        # return name, venue, picture
        return name, venue, picture

    def get_guest_info(self):
        if not os.path.exists(self.record_file):
            # If the file doesn't exist, create one.
            fobj = open(self.record_file, 'w')
            fobj.close()
        self.list_update()
        with open(self.record_file, 'r') as f:
            data = f.readlines()
            json_list_processed = ''.join(data).split('\n')
            f.close()
        new_json = list(i for i in self.json_list if i not in json_list_processed)  # Pick our the new json file received.

        if len(new_json) != 0:  # If there is new json received.
            new_json = new_json[0]  # Currently we just suppose that each checking loop, there will be at most one json file received.
            print(new_json)
            self.insert_tolist(new_json)  # Insert the new file name to the firts line in json file
            name, venue, pic = self.parse_json(new_json)
            return name, venue, pic


kiosk = Kiosk()

def run_server():
    execute_js(kiosk.node_path)

def update_check():
    while True:
        kiosk.get_guest_info()
        sleep(5)

if __name__ == '__main__':
    """Can be tested using postman. IP: http://localhost:3000/api/save. The body sample is included under kisok-pc-robot."""
    t_kiosk = threading.Thread(target=update_check, args=())
    t_server = threading.Thread(target=run_server, args=())
    t_kiosk.start()
    t_server.start()
    t_kiosk.join()
    t_server.join()

