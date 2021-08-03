#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Android autotest """ 
import sys
import subprocess
import re
from time import sleep
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
    exec_adb('shell keyevent %s' % keyevent)

def start_activity(text):
    exec_adb('shell am  start -n %s' % text)

def stop_activity(text):
    exec_adb('shell am  force-stop %s' % text)

def page_on_click(text,t_type='text'):
    dump_layout()
    ret = read_bounds(text,t_type)
    if ret is not None:
        print("Hit:{0}".format(text))
        a,b,c,d = map(int,ret)
        print('a={0},b={1},c={2},d={3}'.format(a,b,c,d))
        on_click(a,b)
    else:
        print("WARN:can not find {0}".format(text))

def page_check_value(text, t_type, attr):
    dump_layout()
    return read_value(text,t_type,attr)

def voice_match_stress(debug):
    if debug == 0 :
        exec_adb('root')
        exec_adb('remount')

        #C:\Users\johl\Desktop>adb shell  dumpsys  activity | findstr  "mFocused"
        #  mFocusedApp=ActivityRecord{f526d53 u0 com.google.android.googlequicksearchbox/com.google.android.apps.gsa.velvet.ui.settings.SettingsActivity t60}
        #    mFocusedWindow=Window{1ceb8f9 u0 com.google.android.googlequicksearchbox/com.google.android.apps.gsa.velvet.ui.settings.SettingsActivity}
        #adb shell am  start -n  com.google.android.googlequicksearchbox/com.google.android.apps.gsa.velvet.ui.settings.SettingsActivity
        #stop_activity('com.google.android.googlequicksearchbox/com.google.android.apps.gsa.velvet.ui.settings.SettingsActivity')
        
        page_on_click('More')
        page_on_click('Settings')
        start_activity('com.google.android.googlequicksearchbox/com.google.android.apps.gsa.velvet.ui.settings.SettingsActivity')
        page_on_click('Voice')
        page_on_click('Voice Match')
        page_on_click('No thanks')
        page_on_click('Hey Google')
        ret = page_check_value('com.google.android.googlequicksearchbox:id/itemview_control_switch','resource-id','checked')
        if ret == 'true': 
            page_on_click('Next')
            page_on_click('I agree')
            page_on_click('Continue')
            page_on_click('Voice model')
            page_on_click('Retrain voice model')
            for i in range(4):
                exec_sox_plbk('./ok_google_one_trigger_short.wav')
                sleep(2)
            page_on_click('Finish')
            page_on_click('Cancel')
        else:
            sleep(3)
            page_on_click('OK')
        
        #back 
        page_on_click('Navigate up','content-desc')

        if 0 :
            pattern = re.compile(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]')
            ret = pattern.match('[0,598][2557,635]')
            print(ret)
            print(ret.groups())
            print(ret.group(0))
            print(ret.group(1))
            print(ret.group(2))
            print(ret.group(3))
            print(ret.group(4))
            print(ret.string)
            print(map(int,ret.groups()))

        #stop_activity('com.google.android.googlequicksearchbox/com.google.android.apps.gsa.velvet.ui.settings.SettingsActivity')

        #adb shell getevent  -p | grep -e "0035" -e "0036
        # $ adb shell getevent  -p | grep -e "0035" -e "0036"
        #                 0035  : value 0, min 0, max 1600, fuzz 0, flat 0, resolution 0
        #                 0036  : value 0, min 0, max 2560, fuzz 0, flat 0, resolution 0
        #                 0035  : value 0, min 0, max 2644, fuzz 0, flat 0, resolution 31
        #                 0036  : value 0, min 0, max 1440, fuzz 0, flat 0, resolution 31
        #                 0031  0032  0033  0034  0035  0036  0037  0038

        #adb shell getevent  | grep -e "0035" -e "0036"
        print("doneI")
    else: 
        #x = subprocess.check_output("adb devices")
        #print(x)
        dump_layout()
        page_check_value('com.google.android.googlequicksearchbox:id/itemview_control_switch','resource-id','checked')

        print("doneE")

if __name__ == "__main__":
    debug = 0
    loop_cnt = 1
    if len(sys.argv) > 1 :
        debug = int(sys.argv[1])
    if len(sys.argv) > 2 :
        loop_cnt = int(sys.argv[2])
    if debug == 0 :
        #print(loop_cnt)
        for i in range(loop_cnt):
            voice_match_stress(debug)
    else:
       voice_match_stress(debug)
