
/*!
 * @file getTime.ino
 * @brief 运行这个例程，先设置内部时钟，在循环获取时钟和温度电压数据
 * @copyright    Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license      The MIT License (MIT)
 * @author       [TangJie](jie.tang@dfrobot.com)
 * @version      V1.0.0
 * @date         2022-07-27
 * @url         https://github.com/DFRobot/DFRobot_SD3031
 */
#include "DFRobot_SD3031.h"

DFRobot_SD3031 rtc;
void setup()
{
    Serial.begin(115200);
    /*Wait for the chip to be initialized completely, and then exit*/
    while(rtc.begin() != 0){
        Serial.println("Failed to init chip, please check if the chip connection is fine. ");
        delay(1000);
    }
    rtc.setHourSystem(rtc.e24hours);//设置显示格式
    rtc.setTime(2021,7,27,14,59,0);//初始化时间
    // //获取内部温度
    // Serial.print(rtc.getTemperatureC());
    // Serial.println(" C");
    // //获取电池电压
    // Serial.print(rtc.getVoltage());
    // Serial.println(" V");
}

void loop()
{
    
    sTimeData_t sTime;
    sTime = rtc.getRTCTime();
    Serial.print(sTime.year, DEC);//year
    Serial.print('/');
    Serial.print(sTime.month, DEC);//month
    Serial.print('/');
    Serial.print(sTime.day, DEC);//day
    Serial.print(" (");
    Serial.print(sTime.week);//week
    Serial.print(") ");
    Serial.print(sTime.hour, DEC);//hour
    Serial.print(':');
    Serial.print(sTime.minute, DEC);//minute
    Serial.print(':');
    Serial.print(sTime.second, DEC);//second
    Serial.println(' ');
    /*12小时时制启用*/
    // Serial.print(rtc.getAMorPM());
    // Serial.println();
    delay(1000);
}
