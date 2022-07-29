#-*- coding: utf-8 -*-
'''!
  @file  interrupt.py
  @brief  设置中断定时，触发中断进行打印
  @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license The MIT License (MIT)
  @author [TangJie](jie.tang@dfrobot.com)
  @version V1.0
  @date 2022-07-25
  @url https://github.com/DFRobot/DFRobot_SD3031
'''
from __future__ import print_function
import sys
sys.path.append('../')
import time
import threading
import RPi.GPIO as GPIO
from DFRobot_SD3031 import *

rtc = DFRobot_SD3031(bus=1)

GPIO.setmode(GPIO.BCM)
flag = 0

#begin return True if succeed, otherwise return False
while not rtc.begin():
    time.sleep(2)

'''
@brief Set mode of time
@param mode H24hours, H12hours
'''
rtc.set_hour_system(rtc.H12hours)

'''
    @brief Set the last compiled time as the current time
'''
#rtc.set_hour_system(rtc.H12hours)
rtc.set_time(year=2022,month=7,day=27,week=rtc.eWednesday,hour=12,minute=59,second=55)

'''
    @brief 中断触发选择和中断时间设置
'''
rtc.set_alarmnumber(trigger=rtc.eHoursEnable, year = 2022, month=7, day=27, week=rtc.eWednesday, hour=13, minute=59, second=0)


IO1 = 21#set interrupt pin

def IO1_callback(channel):#callback function
    rtc.clear_alarm()
    print("Alarm clock is triggered.")
 
GPIO.setup(IO1, GPIO.IN)
'''
@brief When IO1 changes to high level from low level and a FALLING level transition occurs, way to run IO1_callback 
'''
GPIO.add_event_detect(IO1, GPIO.FALLING, callback = IO1_callback)

def main():
    while True:
        rtc.get_time()
        print("{0}/{1}/{2},{3},{4}:{5}:{6} {7}".format(rtc.year,rtc.month,rtc.day,rtc.week,rtc.hour,rtc.minute,rtc.second,rtc.get_AM_or_PM()))#print now time
        print(" ")
        rtc.clear_alarm()
        time.sleep(1)

if __name__ == "__main__":
    main()
