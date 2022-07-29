
/*!
 * @file getTimeAndTemperature.ino
 * @brief 运行这个例程，对RTC模块中RAM数据进行读写
 * @copyright    Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence      The MIT License (MIT)
 * @author       [TangJie](jie.tang@dfrobot.com)
 * @version      V1.0.0
 * @date         2022-07-27
 * @url         https://github.com/DFRobot/DFRobot_SD3031
 */
#include "DFRobot_SD3031.h"

DFRobot_SD3031 rtc;
void setup()
{
    uint8_t data= 0;
    Serial.begin(115200);
    /*Wait for the chip to be initialized completely, and then exit*/
    while(rtc.begin() != 0){
        Serial.println("Failed to init chip, please check if the chip connection is fine. ");
        delay(1000);
    }
    rtc.writeSRAM(0x2b,2);
    //rtc.enable32k();
    delay(1000);
    //rtc.disable32k();
    data = rtc.readSRAM(0x2b);
    Serial.print("data:");
    Serial.println(data);
    delay(100);
    rtc.clearSRAM(0x2b);
    delay(100);
    data = rtc.readSRAM(0x2C);
    Serial.print("data:");
    Serial.println(data);
    
}

void loop()
{
    delay(1000);
}
