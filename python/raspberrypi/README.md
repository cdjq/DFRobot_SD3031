# DFRobot_SD3031
* [中文版](./README_CN.md)

SD3031是一款低成本、极其精确的I2C实时时钟(RTC)模块。在整个温度范围和寿命范围内，可提供±5%ppm的精度(误差不超过0.432s)，并兼容2.5-5.5V宽电压范围。电池供电时，该模块的电流消耗低至2uA。该模块可用于测量环境温度，精度为±3℃。

![产品实物图](../../resources/images/DFR0998.png)


## 产品链接 (https://www.dfrobot.com.cn)
    SKU: DFR0998


## 目录

* [概述](#概述)
* [库安装](#库安装)
* [方法](#方法)
* [兼容性](#兼容性)
* [历史](#历史)
* [创作者](#创作者)


## 概述

* 获取实时，初始时间需要用户设定，我们可以获取编译时间，NTP时间或自己设定，最小单位:s 
* 设置闹钟，用户可以设置两个闹钟，可以在中断引脚处得到下降沿脉冲触发闹钟
* 测量芯片温度，误差:±0.5℃


## 库安装

本库使用到了modbus_tk, 使用本库前先检测树莓派是否成功导入modbus_tk, 若导入失败, 请通过以下命令安装modbus_tk库
python2: pip install modbus_tk
python3: pip3 install modbus_tk

使用库, 首先下载库文件, 将其粘贴到指定的目录中, 然后打开Examples文件夹并在该文件夹中运行演示。


## 方法

```python

    def begin(self):
        '''!
            @brief 初始化芯片
            @return True表示IIC沟通成功，false表示失败。
        '''
 
    def set_hour_system(self, mode = H24hours):
        '''!
            @brief 设置小时时间的输出模式
            @param mode 24小时制, 12小时制; 默认24小时制
        '''

    def set_time(self, year, month, day, week, hour, minute, second):
        '''!
            @brief 设置rtc时间并立即生效
            @param year 1900~2100
            @param month 1~12
            @param date 1~31
            @param week 0~6
            @param hour 0~23
            @param minute 0~59
            @param second 0~59
        '''

    def get_time(self):
        '''!
            @brief 获取RTC时间
        '''

    def clear_alarm(self):
        '''!
          @brief 清楚中断标志位
        '''

    def set_alarmnumber(self,trigger, year, month, day, week, hour, minute, second):
        '''!
            @brief 设置中断时间
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

    def get_temperature_C(self):
        '''!
            @brief 获取芯片内部温度
            @return 返回温度
        '''


    def get_voltage(self):
        '''!
            @brief 获取电池电压
            @return 返回获取得电压
        '''

    def get_AM_or_PM(self):
        '''!
            @brief 输出上午或下午的时间
            @return 上午或下午的时间，24小时模式返回空字符串
        '''

    def enable_32k(self):
        '''!
            @brief 开启32k频率输出
        '''

    def disable_32k(self):
        '''!
            @brief 关闭32k输出
        '''

    def write_SRAM(self, addr, data):
        '''!
            @brief 将数据写入SD3031的SRAM中
            @param addr 存储器地址
            @param data 写数据
        '''

    def read_SRAM(self, addr):
        '''!
            @brief 从SD3031的SRAM中读取数据
            @param addr 存储器地址M
            @return 存储在SRAM中的数据
        '''

    def clear_SRAM(self, addr):
        '''!
            @brief 清除DS3232 SRAM上的数据
            @param addr 存储器地址
        '''

```


## 兼容性

* RaspberryPi版本

| Board        | 正常运行  | 运行失败   | 未测试    | 备注
| ------------ | :-------: | :--------: | :------: | :-----: |
| RaspberryPi2 |           |            |    √     |         |
| RaspberryPi3 |           |            |    √     |         |
| RaspberryPi4 |     √     |            |          |         |

* Python版本

| Python  | 正常运行  | 运行失败   | 未测试    | 备注
| ------- | :-------: | :--------: | :------: | :-----: |
| Python2 |     √     |            |          |         |
| Python3 |     √     |            |          |         |


## 历史

- 2022/07/29 - 1.0.0 版本


## 创作者

Written by TangJie(jie.tang@dfrobot.com), 2021. (Welcome to our [website](https://www.dfrobot.com/))

