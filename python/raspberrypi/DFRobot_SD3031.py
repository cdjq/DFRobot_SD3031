#-*- coding: utf-8 -*-
'''!
  @file  DFRobot_SD3031.py
  @brief  这是一个RTC时钟模块得库
  @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license The MIT License (MIT)
  @author [TangJie](jie.tang@dfrobot.com)
  @version V1.0
  @date 2022-07-25
  @url https://github.com/DFRobot/DFRobot_SD3031
'''
import sys
import time

import smbus
import spidev
import RPi.GPIO as GPIO

import logging
from ctypes import *

class DFRobot_SD3031():
    H24hours            = 0
    H12hours            = 1
    SD3031_IIC_ADDRESS     =0x32  #传感器设备地址
    SD3031_REG_SEC           =0x00  #时钟秒寄存器
    SD3031_REG_MIN           =0x01  #时钟分寄存器
    SD3031_REG_HOUR          =0x02  #时钟小时寄存器
    SD3031_REG_WEEK          =0x03  #时钟星期寄存器
    SD3031_REG_DAY           =0x04  #时钟日寄存器
    SD3031_REG_MONTE         =0x05  #时钟月寄存器
    SD3031_REG_YEAR          =0x06  #时钟年寄存器
    SD3031_REG_ALARM_SEC     =0x07  #时钟秒报警寄存器
    SD3031_REG_ALARM_MIN     =0x08  #时钟分报警寄存器
    SD3031_REG_ALARM_HOUR    =0x09  #时钟小时报警寄存器
    SD3031_REG_ALARM_WEEK    =0x0A  #时钟星期报警寄存器
    SD3031_REG_ALARM_DAY     =0x0B  #时钟日报警寄存器
    SD3031_REG_ALARM_MONNTE  =0x0C  #时钟月报警寄存器
    SD3031_REG_ALARM_YEAR    =0x0D  #时钟年报警寄存器
    SD3031_REG_ALARM_CON     =0x0E  #时钟报警控制寄存器
    SD3031_REG_CTR1          =0x0F  #控制寄存器1
    SD3031_REG_CTR2          =0x10  #控制寄存器2
    SD3031_REG_CTR3          =0x11  #控制寄存器3
    SD3031_REG_TEMP          =0x16  #内部温度寄存器
    SD3031_REG_IIC_CON         =0x17  #IIC控制
    _mode = 0
    _year = 0
    _hours = 0
    year = 0
    month = 0
    day = 0
    week ="Monday"
    hour = 0
    minute = 0
    second = 0
    eSunday    = 0
    eMonday    = 1
    eTuesday   = 2
    eWednesday = 3
    eThursday  = 4
    eFriday    = 5
    eSaturday  = 6
    eYearEnable = 0x40                    
    eMondayEnable = 0x20                  
    eDayEnable = 0x10           
    eHoursEnable = 0x04      
    eMinuteEnable = 0x02
    eSecondEnable =0x01


    def __init__(self, bus):
        '''!
            @brief Module IIC communication init
            @param bus IIC communication bus
        '''
        self.i2cbus=smbus.SMBus(bus)
        self.i2c_addr = self.SD3031_IIC_ADDRESS
    def begin(self):
        '''!
            @brief Init chip
            @return True means IIC communication succeeds, false means it fails.
        '''
        if not self._scan():
            return False
        else:
            return True
    def set_hour_system(self, mode = H24hours):
        '''!
            @brief Set mode of time
            @param mode H24hours, H12hours
        '''
        self._mode = mode
    def set_time(self, year, month, day, week, hour, minute, second):
        '''!
            @brief Set time into rtc and take effect immediately
            @param year 1900~2100
            @param month 1~12
            @param date 1~31
            @param week 0~6
            @param hour 0~23
            @param minute 0~59
            @param second 0~59
        '''
        self._year = year-2000
        if self._mode == 0:
            self._hours = self.bin2bcd(hour)
        else:
            if hour == 0:
                self._hours = 0x12
            elif hour >0 and hour < 12:
                self._hours = (0x00|self.bin2bcd(hour))
            elif hour == 12:
                self._hours = 0x32
            elif hour >12 and hour < 24:
                self._hours = (0x20|self.bin2bcd(hour - 12))

        self.buffer = [self.bin2bcd(second),self.bin2bcd(minute),self._hours,self.bin2bcd(week),self.bin2bcd(day),self.bin2bcd(month),self.bin2bcd(self._year)]
        self._write_reg(self.SD3031_REG_SEC,self.buffer)
        buffer=self._read_reg(self.SD3031_REG_SEC,19)

    def get_time(self):
        '''!
            @brief 获取RTC时间
        '''
        self.buffer = self._read_reg(self.SD3031_REG_SEC,7)
        self.year = 2000+self.bcd2bin(self.buffer[6])
        self.month = self.bcd2bin(self.buffer[5])
        self.day   = self.bcd2bin(self.buffer[4])
        self.data = self.bcd2bin(self.buffer[3])
        if self.data == 0:
            self.week = "Sunday"
        elif self.data ==1:
            self.week = "Monday"
        elif self.data ==2:
            self.week = "Tuesday"
        elif self.data ==3:
            self.week = "Wednesday"
        elif self.data ==4:
            self.week = "Thursday"
        elif self.data ==5:
            self.week = "Friday"
        elif self.data ==6:
            self.week = "Saturday"
        self.data = self.buffer[2]
        if self._mode == 0:
            self.hour = self.bcd2bin(self.data&0x7f)
        else:
            if (self.data&0x20) == 0x20:
              self.data =   self.data & 0x1f
              self.hour = self.bcd2bin(self.data)
            else:
                self.data =   self.data & 0x1f
                self.hour = self.bcd2bin(self.data)

        self.minute = self.bcd2bin(self.buffer[1])
        self.second = self.bcd2bin(self.buffer[0])

    def clear_alarm(self):
        '''!
          @brief clear alarm flag trigger
        '''
        buffer=self._read_reg(self.SD3031_REG_SEC,19)


    def set_alarmnumber(self,trigger, year, month, day, week, hour, minute, second):
        '''!
            @brief Set alarm1 clock
            @param trigger 中断类型选择
            @param year 1900~2100
            @param month 1~12
            @param date 1~31
            @param week 0~6
            @param hour 0~23
            @param minute 0~59
            @param second 0~59
            @return None
        '''
        self._write_reg_byte(self.SD3031_REG_CTR3,0x80)
        self._write_reg_byte(self.SD3031_REG_CTR2,0x92)
        self._year = year-2000
        
        if hour == 0:
            self._hours = 0x12
        elif hour >0 and hour < 12:
            self._hours = (0x00|self.bin2bcd(hour))
        elif hour == 12:
            self._hours = 0x32
        elif hour >12 and hour < 24:
            self._hours = (0x20|self.bin2bcd(hour - 12))

        self.buffer = [self.bin2bcd(second),self.bin2bcd(minute),self._hours,1<<week,self.bin2bcd(day),self.bin2bcd(month),self.bin2bcd(self._year),trigger]
        self._write_reg(self.SD3031_REG_ALARM_SEC,self.buffer)
        buffer=self._read_reg(self.SD3031_REG_SEC,19)

    def get_temperature_C(self):
        '''!
            @brief get temperature of sensor
            @return temperature
        '''

        buffer = self._read_reg(self.SD3031_REG_SEC,23)
        return buffer[22]

    def get_voltage(self):
        '''!
            @brief 获取电池电压
            @return 返回获取得电压
        '''
        buffer = self._read_reg(self.SD3031_REG_SEC,27)
        data =  ((buffer[25]&0x80)<<8)|buffer[26]
        data = data/100.0
        return data

    def get_AM_or_PM(self):
        '''!
            @brief output AM or PM of time 
            @return AM or PM, 24 hours mode return empty string
        '''
        buffer = self._read_reg(self.SD3031_REG_SEC,7)
        data = buffer[2]&0x20
        if data == 0x20:
            return "PM"
        else:
            return "AM"
    
    def enable_32k(self):
        '''!
            @brief enable the 32k output
        '''
        buffer = self._read_reg(self.SD3031_REG_SEC,18)
        staReg = buffer[17]&0x00
        self._write_reg_byte(self.SD3031_REG_CTR3, staReg)

    def disable_32k(self):
        '''!
            @brief disable the 32k output (default is enabled)
        '''
        buffer = self._read_reg(self.SD3031_REG_CTR3)
        staReg = buffer[17]&0x40
        self._write_reg_byte(self.SD3031_REG_CTR3, staReg)

    def write_SRAM(self, addr, data):
        '''!
            @brief write data into the SRAM
            @param addr address of SRAM
            @param data Written data
        '''
        self._write_reg_byte(addr, data)

    def read_SRAM(self, addr):
        '''!
            @brief read data of the SRAM
            @param addr address of SRAM
            @return Read the data
        '''
        return self._read_reg(addr)

    def clear_SRAM(self, addr):
        '''!
            @brief clear the SRAM
            @param addr address of SRAM
        '''
        self._write_reg_byte(addr, 0)


    def bcd2bin(self, val):
        '''!
            @brief BCD code to BIN code
            @param val Input BCD code
            @return Return BIN code
        '''
        return val - 6 * (val >> 4)

    def bin2bcd (self, val):
        '''!
            @brief BIN code to BCD code
            @param val Input BIN code
            @return Return BCD code
        '''
        return val + 6 * int(val / 10)

    def _scan(self):
        '''!
            @brief Scan IIC devices
            @return True means IIC communication succeeds, false means it fails.
        '''
        try:
            self.i2cbus.write_quick(self.i2c_addr)
            self._write_reg_byte(self.SD3031_REG_IIC_CON, 0x80)
            return True
        except:
            print("I2C init fail")
            return False
    
    def _write_reg_byte(self, reg, buff):
        '''!
            @brief writes data to a register
            @param reg register address
            @param buff written data
        '''
        self.i2cbus.write_byte_data (self.i2c_addr, self.SD3031_REG_CTR2, 0x80)
        time.sleep(0.01)
        self.i2cbus.write_byte_data (self.i2c_addr, self.SD3031_REG_CTR1, 0xff)
        time.sleep(0.01)
        self.i2cbus.write_byte_data(self.i2c_addr, reg, buff)
        time.sleep(0.01)
        self.i2cbus.write_byte_data (self.i2c_addr, self.SD3031_REG_CTR1, 0x7B)
        time.sleep(0.01)
        self.i2cbus.write_byte_data (self.i2c_addr, self.SD3031_REG_CTR2, 0x12)

    def _write_reg(self, reg, buff):
        '''!
            @brief writes data to a register
            @param reg register address
            @param buff written data
        '''
        self.i2cbus.write_byte_data (self.i2c_addr, self.SD3031_REG_CTR2, 0x80)
        time.sleep(0.01)
        self.i2cbus.write_byte_data (self.i2c_addr, self.SD3031_REG_CTR1, 0xff)
        time.sleep(0.01)
        self.i2cbus.write_i2c_block_data(self.i2c_addr, reg, buff)
        time.sleep(0.01)
        self.i2cbus.write_byte_data (self.i2c_addr, self.SD3031_REG_CTR1, 0x7B)
        time.sleep(0.01)
        self.i2cbus.write_byte_data (self.i2c_addr, self.SD3031_REG_CTR2, 0x12)
        

    def _read_reg(self, reg, length):
        '''!
            @brief read the data from the register
            @param reg register address
            @return Read the register data
        '''
        return self.i2cbus.read_i2c_block_data(self.i2c_addr, reg, length) 
