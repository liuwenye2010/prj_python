#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import win32gui   #come from pywin32
import win32con   #come from pywin32
import win32api   #come from pywin32
#from pymouse import PyMouse
#from pykeyboard import PyKeyboard
#from pywinauto import application
#import SendKeys  #pip install SendKeys
import time
import uiautomation  #pip install uiautomation
import uiautomation as automation
import subprocess 
import unittest
import logging
import time
import os

def win32_keyevent(): 
    win32api.keybd_event(17, 0, 0, 0)  # 键盘按下 Ctrl
    time.sleep(1)
    win32api.keybd_event(82, 0, 0, 0)  # 键盘按下  82 R
    time.sleep(1)
    win32api.keybd_event(82, 0, win32con.KEYEVENTF_KEYUP, 0)  # 键盘松开  82 R
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 键盘松开  17 Ctrl

def win32_mouse():
    # 鼠标单击事件
    #鼠标定位到(30,50)
    win32api.SetCursorPos([30,150])
    #执行左单键击
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    #右键单击
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)

def win32_automation():

    print(automation.GetRootControl())
    subprocess.Popen('notepad.exe')
    notepadWindow = automation.WindowControl(searchDepth = 1, ClassName = 'Notepad')
    print(notepadWindow.Name)
    notepadWindow.SetTopmost(True)
    edit = notepadWindow.EditControl()
    #edit.SetValue('Hello')
    edit.SendKeys('{Ctrl}{End}{Enter}World')


class TestFaultTree(unittest.TestCase):
    def setUp(self) -> None:
        os.system("calc")
        time.sleep(2)
        self.calc = uiautomation.WindowControl(Name="Calculator")
        self.calc_list = ["Two", "Plus", "Eight", "Equals"]
        self.result = "10"


    def tearDown(self) -> None:
        time.sleep(1)
        self.calc.ButtonControl(Name="Close Calculator").Click()


    def test_toolbar(self):

        time.sleep(1)
        for i in range(0, len(self.calc_list)):
            self.calc.ButtonControl(Name=self.calc_list[i]).Click()
            time.sleep(0.2)

        calc_result = self.calc.TextControl(foundIndex=3).Name
        print("Run:", calc_result)
        print("Expect：", self.result)
        self.assertIn(self.result, calc_result)

if __name__ == "__main__":
    print("py_win32")
    #win32_keyevent()
    #win32_automation()
    unittest.main()
    pass