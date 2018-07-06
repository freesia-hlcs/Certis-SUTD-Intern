import speech_recognition as sr
import os
import sys
import wave
import numpy as np
from pyaudio import PyAudio, paInt16
import keyboard
import xlrd
import xlwt
import xlutils
from xlutils.copy import copy as xcopy
module_path = os.getcwd().replace('\\', '/')+'/AzureApi/'
sys.path.append(module_path)
from CreateProfile import create_profile #create_profile(subscription_key, locale
from DeleteProfile import delete_profile #delete_profile(subscription_key, profile_id)
from EnrollProfile import enroll_profile #enroll_profile(subscription_key, profile_id, file_path, force_short_audio)
from GetProfile import get_profile #get_profile(subscription_key, profile_id)
from IdentifyFile import identify_file #identify_file(subscription_key, file_path, force_short_audio, profile_ids)
from PrintAllProfiles import print_all_profiles #print_all_profiles(subscription_key
from ResetEnrollments import reset_enrollments #reset_enrollments(subscription_key, profile_id)
import IdentificationServiceHttpClientHelper
import time

#from 文件夹 import 文件名.函数名 (需要在文件夹里建好__init__.py)

r = sr.Recognizer()
subscription_key = '47bfaa2bbd704085a369ef7c17f4daef'
helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

class speaker_identification(object):
    def __init__(self):
        self.num_samples = 2000  # pyaudio内置缓冲大小
        self.sampling_rate = 16000  # 取样频率
        self.level = 1500  # 声音保存的阈值
        self.count_num = 20  # count_num个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
        self.save_length = 8  # 声音记录的最小长度：save_length * num_samples 个取样
        self.voice_string = []
        self.profile_file = 'profile_info.xls'

    # 保存文件
    def save_wav(self, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.sampling_rate)
        wf.writeframes(np.array(self.voice_string).tostring())
        wf.close()

    def read_audio(self):
        pa = PyAudio()
        keyboard.wait('space')
        stream = pa.open(format=paInt16, channels=1, rate=self.sampling_rate, input=True,
                         frames_per_buffer=self.num_samples)

        save_count = 0
        save_buffer = []
        while True:
            # 读入num_samples个取样
            string_audio_data = stream.read(self.num_samples)
            # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            # 计算大于 level 的取样的个数
            large_sample_count = np.sum(audio_data > self.level)

            print(np.max(audio_data)), "large_sample_count=>", large_sample_count

            # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            if large_sample_count > self.count_num:
                save_count = self.save_length
            else:
                save_count -= 1
            if save_count < 0:
                save_count = 0

            if save_count > 0:
                save_buffer.append(string_audio_data)
            else:
                if len(save_buffer) > 0:
                    self.voice_string = save_buffer
                    save_buffer = []
                    print("Recode a piece of  voice successfully!")
                    return True

            if keyboard.is_pressed('space'):
                if len(save_buffer) > 0:
                    self.voice_string = save_buffer
                    save_buffer = []
                    print("Recode a piece of  voice successfully!")
                    return True
                else:
                    return False
        return True

    # def record_voice(self):
    #     self.read_audio()
    #     self.save_wav("./test_reocrd.wav")

    def model_train(self,name):
        profile_id = create_profile(subscription_key, 'en-US')
        profile_info = {name: profile_id}
        self.profile_save(profile_info)
        print("Console: The guest's info has been created: ", profile_info)
        file_name = 'test_reocrd.wav'
        self.read_audio()
        self.save_wav("./"+file_name)
        output = enroll_profile(subscription_key, profile_id, file_name, 'True')
        print("Console: {}({})'s profile is enrolled successfully.".format(name, profile_id))
        return output

    def profile_save(self,profile_info):
        readbook = xlrd.open_workbook('profile_info.xls')
        table = readbook.sheets()[0] #What if we use the sheet as a claasifier tool?
        #大部分人让我学着去看世俗的眼光
        nrows = table.nrows
        ncols = table.ncols

        workbook = xcopy(readbook)
        writesheet = workbook.get_sheet(0)
        writesheet.write(nrows, 0, list(profile_info.keys())[0])
        writesheet.write(nrows, 1, list(profile_info.values())[0])
        workbook.save('profile_info.xls')


    def speech_identify(self):
        pass
        # with open(file_path, 'rb') as body:
        #需要对excel进行检索


def vocie_register(name):
    profile_id = create_profile(subscription_key,'en-US')
    print("Your info has been created: ", {name:profile_id})
    #{'Wang Cheng': '8a6c92cf-451d-477b-878e-71530fc0a0d6'}
    #Tang_Xinran(3a6c906e-c357-4305-af3b-1c47e579c91c)
    return profile_id

count = 1
def record_file(name,profile_id):
    # write audio to a WAV file
    global count
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        temp = audio.get_wav_data(convert_rate=16000)
    file_name = name +"_"+str(count)+ ".wav"
    with open(file_name , "wb") as f:
        f.write(temp)
        print('The file is saved.')
    check = input("Is the reocoring okay? (Y/n)")
    if check == 'Y':
        if count <= 2:
            count += 1
            enroll_profile(subscription_key, profile_id, file_name, 'True')
            print('Still need to record {} times.'.format(str(4-count)))
            return record_file(name,profile_id)
        else:
            print("{}({})'s profile is enrolled successfully.".format(name,subscription_key))
            return enroll_profile(subscription_key, '8a6c92cf-451d-477b-878e-71530fc0a0d6', file_name, 'True')
    elif check == 'n':
        return record_file(name,profile_id)
time1,time2,time3,time4,time5 = 0.0,0.0,0.0,0.0,0.0
def identification(profile_ids):
    global time1,time2,time3,time4,time5
    file_name = 'test_file.wav'
    time1 = time.time()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        temp = audio.get_wav_data(convert_rate=16000)
        #identify_file(subscription_key, file_path, force_short_audio, profile_ids)
    time2 = time.time()

    with open(file_name , "wb") as f:
        f.write(temp)
        print('The file is saved.')
    time3 = time.time()
    check = input("Is the reocoring okay? (Y/n)")
    if check == 'Y':
        time4 = time.time()
        response = identify_file(subscription_key, file_name, 'True', profile_ids)
        time5 = time.time()
        return response['Identified Speaker']
    elif check == 'n':
        return identification(profile_ids)
    #提高速度的方法：多线程，减少文件存储与读取时间




def main():
    name = input('Name: ')
    profile_id  = vocie_register(name)
    # name = 'Wang Cheng'
    eidted_name = name.replace(' ','_')
    record_file(eidted_name,profile_id)
    profile_info = {"Wang Cheng":"8a6c92cf-451d-477b-878e-71530fc0a0d6","Tang Xinran":"3a6c906e-c357-4305-af3b-1c47e579c91c",'Mei Mei':"34172e8b-7b20-4553-9c4d-f9acf67e854c"}
    profile_id_lis = list(profile_info.values())
    profile_ids = profile_id_lis[0]
    for id in profile_id_lis[1:]:
        profile_ids += ',{}'.format(id)
    speaker_id = identification(profile_id_lis)
    print('The speaker is {}.'.format(list(profile_info.keys())[list(profile_info.values()).index(speaker_id)]))
    print(time2-time1,time3-time2,time4-time3,time5-time4)

if __name__ == '__main__':
    # r = GenAudio()
    # r.read_audio()
    # r.save_wav("./test_reocrd.wav")
    main()