#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Android autotest """ 
import sys
import subprocess
import re
import os
from time import sleep
import unittest
import uiautomator2 as u2
from lxml import etree

PACKAGE_NAME = "com.google.android.googlequicksearchbox"

def get_device_handle():
    #readDeviceId = list(os.popen('adb devices').readlines())
    #print(readDeviceId)
    #deviceId = re.findall(r'^\w*\b', readDeviceId[1])[0]
    #print(deviceId)
    #return u2.connect_usb(deviceId)
    return u2.connect()

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

def is_screen_lock():
    ret = exec_adb("shell dumpsys power | grep 'mHoldingWakeLockSuspendBlocker' | grep -oE '(false|true)'")
    if "true" in str(ret) :
        print("INFO:screen LOCKED")
        return 1
    else:
        print("INFO:screen UNLOCED")
        return 0 

def capture_dmesg():
    exec_adb('root')
    exec_adb('remount')
    exec_adb('push ./codec_parse.sed /data')
    subprocess.Popen('adb shell cat /dev/kmsg  | grep as339 | sed -f /data/codec_parse.sed > /data/dmesg_log.txt ')

def get_dmesg_log():
    exec_adb('pull /data/dmesg_log.txt .')

def closeApp():
    d.app_stop(PACKAGE_NAME)
    #d.app_clear(PACKAGE_NAME)

def voice_match_stress(debug, d):
    exec_adb('root')
    exec_adb('remount')
    if d.info.get('screeOn')==False:
       d.sreen_on()
    #if is_screen_lock() == 0: 
    #    on_key_unlock()
    d.unlock()
    ret_vm  = 0 
    if debug == 0 :
        #on_key_back()
        #on_key_home()
        d.press("back")
        d.press("home")
        d.app_start(PACKAGE_NAME,"com.google.android.apps.gsa.velvet.ui.settings.SettingsActivity")
        print("click Voice btn")
        #d(text="Voice").click()
        sleep(1)
        d(className="android.widget.ListView", resourceId="android:id/list").child_by_text("Voice", className="android.widget.LinearLayout").click()
        if d(text="Voice Match").exists:
            print("click Voice Match btn")
            d(text="Voice Match").click()
        if d(text="No thanks").exists:
            print("click No thanks btn") 
            d(text="No thanks").click()
        else:
            print("No thanks btn doesn't exist")
        if d(text="Hey Google").exists:
            print("click Hey Google btn") 
            d(text="Hey Google").click()
        print("ready to click hey google switch button")
        
        if d(className="android.widget.Button", resourceId="android:id/button3", text="OK").exists:
            print("Click notify OK btn")
            d(text="OK").click()

        rt = False
        if d(resourceId="com.google.android.googlequicksearchbox:id/opa_error_action_button",text="Next").exists:
            print("Next is exists")
            d(text="Next").click()
        else:
            print("Next btn is not exists")
        if d(text="I agree").exists:
            d(text="I agree").click()
        if d(text="'Continue'").exists:
            d(text="'Continue'").click()
            rt = True
            sleep(3)

        if d(resourceId="com.google.android.googlequicksearchbox:id/itemview_control_switch").exists:
            rt = d(resourceId="com.google.android.googlequicksearchbox:id/itemview_control_switch").info.get("checked")
            print(rt)

        if rt== True: 
            print("INFO:Voice Match ON")
            if d(text="Voice model").exists:
                d(text="Voice model").click()
            sleep(1)
            if d(text="Retrain voice model").exists:
                d(text="Retrain voice model").click()
            sleep(2)
            for i in range(4):
                exec_sox_plbk('./ok_google_one_trigger_short.wav')
                sleep(2)
            sleep(3)
            if d(resourceId="com.google.android.googlequicksearchbox:id/opa_error_action_button",text="Finish").exists:
                print("to click Finish btn")
                ret_vm = d(text="Finish").click()
                print(ret_vm)
            else:
                print("ok google trigger failure")
                return -1
            #get_dmesg_log()
        else:
            print("INFO:Voice Match OFF")
            sleep(3)
            if d(text="Next").exists:
                d(text="Next").click()
            if d(text="I agree").exists:
                d(text="I agree").click()
            if d(text="Cancel").exists:
                d(text="Cancel").click()
            if d(text="OK").exists:
                d(text="OK").click()
        #get_dmesg_log()
        closeApp()
        print("doneI")
        return 0
    else: 
        print("debug value is not 0")
        d.app_start(PACKAGE_NAME,"com.google.android.apps.gsa.velvet.ui.settings.SettingsActivity")
        print("doneE")
    print("stop app and clear app")
    closeApp()
    on_key_home()

if __name__ == "__main__":
    d = get_device_handle()
    infos=d.info
    print(infos)
    debug = 0
    loop_cnt = 1
    if len(sys.argv) > 1:
        loop_cnt = int(sys.argv[1])
    if len(sys.argv) > 2 :
        debug = int(sys.argv[2])
    if debug == 0 :
        for i in range(loop_cnt):
            print(i)
            vs_ret = voice_match_stress(debug,d)
            if vs_ret < 0:
                print("FAIL: VOICE_MATCH_TEST FAIL")
                break
    else:
       voice_match_stress(debug,d)
    d.uiautomator.stop()