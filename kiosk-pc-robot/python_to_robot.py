import time
import socket
import json
import os

conne = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
path = os.getcwd()
path.replace("\\" , "/")
record_file = 'record.txt'
file_path = os.getcwd() + '/files/'

#Connect to the robot through local area network.
conne.connect(('192.168.99.93', 7171))#IP address and port number
message = b"adept\n"
conne.send(message) #Send the psw to the robot. (The default one is 'adept')

# while True:
#     recvdata = conne.recv(1024)
#     print(recvdata)
#     if b"End of commands" in recvdata:
#         break

def InsertIntoList(new_json):
    fp = open('Record.txt')
    fp = fp.readlines()
    lines = []
    for line in fp:
        lines.append(line)
    lines.insert(0, new_json + '\n')  # Insert the new file's name in at the first line.
    s = ''.join(lines)
    fp = open('Record.txt', 'w')
    fp.write(s)
    fp.close()

def parz_json(file):
    f = open(file_path + file, encoding='utf-8')
    # Set encoding mode. This parameter needs to be utf-8 or the default mode will be gbk
    content = json.load(f)
    name, venue = content['visitor_name'], content['meeting_venue']
    # picture = file.strip('.json') + '.png'
    # if picture not in pic_list:
    #     print("ERROR:The picture {} is not stored".format(picture))
    # return name,venue,picture
    return name, venue


# def SendToRobot(name,venue,pic):
def SendToRobot(name,venue):
    start = b"New VVVIP\n"
    info = name + ',' + venue + '\n'
    info = info.encode('utf-8')
    end = b'Done\n'
    print("The information of {}'s visit has been sent to the robot.".format(name))


def main():
    if not os.path.exists(record_file):
        #If the file doesn't exist, create one.
        fobj = open(record_file, 'w')
        fobj.close()
    f = open(record_file,'r')
    data = f.readlines()
    json_list_processed = ''.join(data).split('\n')
    f.close()
    json_list = [i for i in os.listdir(file_path) if i.endswith('.json')]
    pic_list = [i for i in os.listdir(file_path) if i.endswith('.png')]
    new_json = list(i for i in json_list if i not in json_list_processed) #Pick our the new json file received.
    if len(new_json) != 0: #If there is new json received.
        new_json = new_json[0]  #Currently we just suppose that each checking loop, there will be at most one json file received.
        # read_json(new_json)
        print(json_list_processed ,json_list, new_json)
        InsertIntoList(new_json)#Insert the new file name to the firts line in json file
        # name,venue,pic = parz_json(new_json)
        # SendToRobot(name,venue,pic)
        name,venue = parz_json(new_json)
        SendToRobot(name,venue)


while True:
    main()



# file = '2018-5-28-14-32_Utaha.json'
#
# read_json(file_path + file)

