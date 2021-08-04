#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Android autotest """ 
import sys
import subprocess
import re
from time import sleep
import unittest
#import uiautomator as ui 
#import uiautomator2 as ui2
#import pysox
from lxml import etree
#from xml.etree.ElementTree import ElementTree



def exec_adb(cmd): 
    return subprocess.check_output(('adb %s'%cmd).split(' '))

def exec_sox_plbk(wav_file):
    subprocess.check_output('sox  {0}  -t waveaudio -d  '.format(wav_file))

def exec_sox_recd(wav):
    pass 

def dump_layout(): 
    exec_adb('root')
    exec_adb('remount')
    exec_adb('shell uiautomator dump /data/temp_ui.xml') 
    exec_adb('pull /data/temp_ui.xml .')

def read_bounds(text,t_type='text'): 
    pattern = re.compile(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]')
    with open('./temp_ui.xml', 'r', encoding='utf-8') as f:
        file_content = f.read()
    if file_content is not None: 
        node_file = etree.XML(file_content.encode('utf-8'))
        node = node_file.xpath(u'//node[@%s="%s"]/@bounds' %(t_type,text))
        if len(node) > 0 :
            bounds_str = node[0]
            match =  pattern.match(bounds_str)
            if(match):
                return match.group(1) , match.group(2),  match.group(3),  match.group(3)
            return bounds_str
        #ret = pattern.match('[0,598][2557,635]')
    return None

def read_value(text,t_type,attr):
    with open('./temp_ui.xml', 'r', encoding='utf-8') as f:
        file_content = f.read()
    if file_content is not None: 
        node_file = etree.XML(file_content.encode('utf-8'))
        node = node_file.xpath(u'//node[@%s="%s"]/@%s' %(t_type,text,attr))
        if len(node) > 0 :
            bounds_str = node[0]
            return bounds_str
        else:
            return None 

def on_click(x, y): 
    exec_adb('shell input tap %d %d' % (x, y))

def perform_scroll(x0, y0, x1, y1, duration): 
    exec_adb('shell input swipe %d %d %d %d %d' % (x0, y0, x1, y1, duration))

def input_text(text): 
    exec_adb('shell input text %s' % text)

def on_keyevent(keyevent):
    exec_adb('shell input keyevent %s' % keyevent)

def start_activity(text):
    exec_adb('shell am  start -n %s' % text)

def stop_activity(text):
    exec_adb('shell am  force-stop %s' % text)

def on_key_home():
    on_keyevent(3)

def on_key_back():
    on_keyevent(4)

def on_key_power():
    on_keyevent(26)

def on_key_unlock():
    #input touchscreen swipe 930 880 930 380 #Swipe UP
    on_keyevent(82)

def is_screen_on():
    ret = exec_adb("shell dumpsys power | grep 'mHoldingDisplaySuspendBlocker' | grep -oE '(false|true)'")
    if "true" in str(ret) :
        print("INFO:screen ON")
        return 1
    else:
        print("INFO:screen OFF")
        return 0 

def is_screen_lock():
    ret = exec_adb("shell dumpsys power | grep 'mHoldingWakeLockSuspendBlocker' | grep -oE '(false|true)'")
    if "true" in str(ret) :
        print("INFO:screen LOCKED")
        return 1
    else:
        print("INFO:screen UNLOCED")
        return 0 

    
def screen_on():
    ret = exec_adb("shell dumpsys power | grep 'Display Power' | grep -oE '(ON|OFF)'")
    if "OFF" in str(ret) :
        on_key_power()
    else:
        pass
def screen_off():
    ret = exec_adb("shell dumpsys power | grep 'Display Power' | grep -oE '(ON|OFF)'")
    if "ON" in str(ret) :
        on_key_power()
    else:
        pass
def capture_dmesg():
    exec_adb('root')
    exec_adb('remount')
    exec_adb('push ./codec_parse.sed /data')
    subprocess.Popen('adb shell cat /dev/kmsg  | grep as339 | sed -f /data/codec_parse.sed > /data/dmesg_log.txt ')



def get_dmesg_log():
    exec_adb('pull /data/dmesg_log.txt .')

def page_on_click(text,t_type='text'):
    dump_layout()
    ret = read_bounds(text,t_type)
    if ret is not None:
        print("Hit:{0}".format(text))
        a,b,c,d = map(int,ret)
        print('a={0},b={1},c={2},d={3}'.format(a,b,c,d))
        on_click(a,b)
        return  1  
    else:
        print("WARN:can not find {0}".format(text))
        return  0

def page_check_value(text, t_type, attr):
    dump_layout()
    return read_value(text,t_type,attr)

def voice_match_stress(debug):
    exec_adb('root')
    exec_adb('remount')
    if is_screen_on() == 0:
        screen_on()
    if is_screen_lock() == 0: 
        on_key_unlock()
    ret_vm  = 0 
    if debug == 0 :
        on_key_home()
        #on_key_back()
        start_activity('com.google.android.googlequicksearchbox/com.google.android.apps.gsa.velvet.ui.settings.SettingsActivity')
        page_on_click('Voice')
        page_on_click('Voice Match')
        page_on_click('No thanks')
        page_on_click('Hey Google')
        ret = page_check_value('com.google.android.googlequicksearchbox:id/itemview_control_switch','resource-id','checked')
        if page_on_click('Next')  > 0:
            page_on_click('I agree')
            ret = 'true'
        if ret == 'true': 
            print("INFO:Voice Match ON")
            #page_on_click('Next')
            #page_on_click('I agree')
            #page_on_click('Continue')
            page_on_click('Voice model')
            page_on_click('Retrain voice model')
            for i in range(4):
                exec_sox_plbk('./ok_google_one_trigger_short.wav')
                sleep(2)
            ret_vm =  page_on_click('Finish')
            if ret_vm == 0:
                return  -1 
        else:
            print("INFO:Voice Match OFF")
            sleep(3)
            page_on_click('Next')
            page_on_click('I agree')
            page_on_click('Cancel')
            page_on_click('OK')
            #on_key_back()
        #page_on_click('Navigate up','content-desc')
        #stop_activity('com.google.android.googlequicksearchbox/com.google.android.apps.gsa.velvet.ui.settings.SettingsActivity')
        #get_dmesg_log()
        print("doneI")
        return 0
    else: 
        dump_layout()
        ##ERR: start_activity('com.google.android.googlequicksearchbox/com.google.android.apps.search.googleapp.activity.GoogleAppActivity')
        start_activity('com.google.android.googlequicksearchbox/com.google.android.apps.gsa.velvet.ui.settings.SettingsActivity')
        #page_check_value('com.google.android.googlequicksearchbox:id/itemview_control_switch','resource-id','checked')
        print("doneE")
    on_key_home()

if __name__ == "__main__":
    debug = 0
    loop_cnt = 1
    if len(sys.argv) > 1:
        loop_cnt = int(sys.argv[1])
    if len(sys.argv) > 2 :
        debug = int(sys.argv[2])
    if debug == 0 :
        #capture_dmesg()
        #print(loop_cnt)
        for i in range(loop_cnt):
            vs_ret = voice_match_stress(debug)
            if vs_ret < 0:
                print("FAIL: VOICE_MATCH_TEST FAIL")
                break
        #get_dmesg_log()
    else:
       voice_match_stress(debug)
