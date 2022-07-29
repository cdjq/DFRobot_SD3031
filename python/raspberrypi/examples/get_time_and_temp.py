#-*- coding: utf-8 -*-
'''!
  @file  get_time_and_temp.py
  @brief  Get the time and temperature of chip
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
from DFRobot_SD3031 import *

rtc = DFRobot_SD3031(bus=1)


#begin return True if succeed, otherwise return False
while not rtc.begin():
    time.sleep(2)

'''
@brief Set mode of time
@param mode H24hours, H12hours
'''
rtc.set_hour_system(rtc.H12hours)

'''
@brief Set time into rtc and take effect immediately
@param year, 1900~2100
@param month, 1~12
@param day, 1~31
@param week, 0~6
@param hour, 0~23
@param minute, 0~59
@param second, 0~59
'''
rtc.set_time(year=2022,month=7,day=29,week=rtc.eWednesday,hour=12,minute=59,second=55)

def main():
    flag = 0
    while True:
        '''
            @brief 获取温度
            @return temperature, unit:℃
        '''
        temp = rtc.get_temperature_C()
        rtc.get_time()
        print("{0}/{1}/{2},{3},{4}:{5}:{6} {7}".format(rtc.year,rtc.month,rtc.day,rtc.week,rtc.hour,rtc.minute,rtc.second,rtc.get_AM_or_PM()))#print now time
        if flag == 59:
            flag = 0
            print(temp)
        print(" ")
        flag=flag+1
        time.sleep(1)

if __name__ == "__main__":
    main()

