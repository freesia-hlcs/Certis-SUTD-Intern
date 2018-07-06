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

class speaker_identification():
    def __init__(self):
        self.num_samples = 2000
        self.sampling_rate = 16000
        self.level = 1500
        self.count_num = 20
        self.save_length = 8
        #↑↑↑setting parameters for audio record
        self.voice_string = []
        self.profile_file = 'profile_info.xls'

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
            string_audio_data = stream.read(self.num_samples)
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            large_sample_count = np.sum(audio_data > self.level)

            print(np.max(audio_data)), "large_sample_count=>", large_sample_count

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
                    # self.voice_string = save_buffer
                    # save_buffer = []
                    # print("Recode a piece of  voice successfully!")
                    # return True
                    pass

            if keyboard.is_pressed('space'):
                if len(save_buffer) > 0:
                    self.voice_string = save_buffer
                    save_buffer = []
                    print("Recode a piece of  voice successfully!")
                    return True
                else:
                    return False
        return True

    def model_train(self,name):
        """
        Create the voice profile info for the guest and finish the basic trainning
        :param name: The name of the speaker whose voice is being input
        :return:voice enroll status
        """
        profile_id = create_profile(subscription_key, 'en-US')
        profile_info = {name: profile_id}
        self.profile_save(profile_info)
        print("Console: The guest's info has been created: ", profile_info)
        file_name = 'test_reocrd.wav'
        self.read_audio()
        self.save_wav("./"+file_name)
        output = enroll_profile(subscription_key, profile_id, file_name, 'True')
        print("Console: {} ({})'s profile is enrolled successfully.".format(name, profile_id))
        return output

    def profile_save(self,profile_info):
        """
        Save profile info in excel
        :param profile_info: name-voice_profile_id pair
        :return:
        """
        readbook = xlrd.open_workbook(self.profile_file)
        table = readbook.sheets()[0] #What if we use the sheet as a claasifier tool?
        # table.row_values(i)
        nrows = table.nrows
        ncols = table.ncols

        workbook = xcopy(readbook)
        writesheet = workbook.get_sheet(0)
        writesheet.write(nrows, 0, list(profile_info.keys())[0])
        writesheet.write(nrows, 1, list(profile_info.values())[0])
        workbook.save('profile_info.xls')


    time1, time2, time3, time4, time5 = 0.0, 0.0, 0.0, 0.0, 0.0
    def speech_identify(self):
        """Identify the speker by compare current sentence with the voice feature stored in Azure server."""
        global time1, time2, time3, time4, time5
        time1 = time.time()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
            temp = audio.get_wav_data(convert_rate=16000)

        readbook = xlrd.open_workbook(self.profile_file)
        table = readbook.sheets()[0]  # What if we use the sheet as a claasifier tool?
        profile_ids = table.col_values(1)
        profile_names = table.col_values(0)
        response = identify_file(subscription_key, temp, 'True', profile_ids)
        speaker_id =  response['Identified Speaker ID']
        speaker_name = profile_names[profile_ids.index(speaker_id)]
        print('Console: {} is speaking.'.format(speaker_name))


def main():
    identify = speaker_identification()
    name = input('pls enter your name: ')
    if name == 'identify':
        while not keyboard.is_pressed('esc'):
            identify.speech_identify()
    elif name == 'reset':
        pass
    else:
        identify.model_train(name)


if __name__ == '__main__':
    while 1:
        main()

