import json
import os


class Kiosk(object):

    def __init__(self):
        self.path = os.getcwd()
        self.path.replace('\\', '/')
        self.record_file = 'Record.txt'
        self.file_path = os.getcwd() + '/files/'

    def insert_into_list(self, new_json):
        fp = open(self.record_file)
        fp = fp.readlines()
        lines = []
        for line in fp:
            lines.append(line)
        lines.insert(0, new_json + '\n')  # Insert the new file's name in at the first line.
        s = ''.join(lines)
        fp = open(self.record_file, 'w')
        fp.write(s)
        fp.close()

    def parse_json(self, file):
        f = open(self.file_path + file, encoding='utf-8')
        # Set encoding mode. This parameter needs to be utf-8 or the default mode will be gbk
        content = json.load(f)
        name, venue = content['visitor_name'], content['meeting_venue']
        # picture = file.strip('.json') + '.png'
        # if picture not in pic_list:
        #     print("ERROR:The picture {} is not stored".format(picture))
        # return name, venue, picture
        return name, venue

    def get_guest_info(self):
        if not os.path.exists(self.record_file):
            # If the file doesn't exist, create one.
            fobj = open(self.record_file, 'w')
            fobj.close()
        f = open(self.record_file, 'r')
        data = f.readlines()
        json_list_processed = ''.join(data).split('\n')
        f.close()
        json_list = [i for i in os.listdir(self.file_path) if i.endswith('.json')]
        pic_list = [i for i in os.listdir(self.file_path) if i.endswith('.png')]
        new_json = list(i for i in json_list if i not in json_list_processed)  # Pick our the new json file received.
        if len(new_json) != 0:  # If there is new json received.
            new_json = new_json[0]  # Currently we just suppose that each checking loop, there will be at most one json file received.
            # read_json(new_json)
            print(json_list_processed, json_list, new_json)
            self.insert_into_list(new_json)  # Insert the new file name to the firts line in json file
            # name, venue, pic = self.parse_json(new_json)
            # return name, venue, pic
            name, venue = self.parse_json(new_json)
            return name, venue

    def get_guest_pic(self):
        img = 'michael2.jpg'
        return img
