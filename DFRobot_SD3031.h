/*!
 * @file DFRobot_SD3031.h
 * @brief DFRobot_SD3031 类的基础结构
 * @details 定义SD3031功能的函数
 * @copyright	Copyright (c) 2021 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license The MIT License (MIT)
 * @author [TangJie](jie.tang@dfrobot.com)
 * @version V1.0
 * @date 2022-07-25
 * @url https://github.com/DFRobot/DFRobot_SD3031
 */
#ifndef _DFROBOT_SD3031_H
#define _DFROBOT_SD3031_H

#include "Arduino.h"
#include "Wire.h"

//#define ENABLE_DBG ///< 打开这个宏, 可以看到程序的详细运行过程
#ifdef ENABLE_DBG
#define DBG(...) {Serial.print("[");Serial.print(__FUNCTION__); Serial.print("(): "); Serial.print(__LINE__); Serial.print(" ] "); Serial.println(__VA_ARGS__);}
#else
#define DBG(...)
#endif
/**
 * @struct sTimeData_t
 * @brief 存储时间数据得结构体
 */
typedef struct{
    uint16_t year;
    uint8_t  month;
    uint8_t  day;
    String   week;
    uint8_t  hour;
    uint8_t minute;
    uint8_t second;
  }sTimeData_t;

class DFRobot_SD3031
{
  #define SD3031_IIC_ADDRESS       0x32  ///< 传感器设备地址
  #define SD3031_REG_SEC           0x00  ///< 时钟秒寄存器
  #define SD3031_REG_MIN           0x01  ///< 时钟分寄存器
  #define SD3031_REG_HOUR          0x02  ///< 时钟小时寄存器
  #define SD3031_REG_WEEK          0x03  ///< 时钟星期寄存器
  #define SD3031_REG_DAY           0x04  ///< 时钟日寄存器
  #define SD3031_REG_MONTE         0x05  ///< 时钟月寄存器
  #define SD3031_REG_YEAR          0x06  ///< 时钟年寄存器
  #define SD3031_REG_ALARM_SEC     0x07  ///< 时钟秒报警寄存器
  #define SD3031_REG_ALARM_MIN     0x08  ///< 时钟分报警寄存器
  #define SD3031_REG_ALARM_HOUR    0x09  ///< 时钟小时报警寄存器
  #define SD3031_REG_ALARM_WEEK    0x0A  ///< 时钟星期报警寄存器
  #define SD3031_REG_ALARM_DAY     0x0B  ///< 时钟日报警寄存器
  #define SD3031_REG_ALARM_MONNTE  0x0C  ///< 时钟月报警寄存器
  #define SD3031_REG_ALARM_YEAR    0x0D  ///< 时钟年报警寄存器
  #define SD3031_REG_ALARM_CON     0x0E  ///< 时钟报警控制寄存器
  #define SD3031_REG_CTR1          0x0F  ///< 控制寄存器1
  #define SD3031_REG_CTR2          0x10  ///< 控制寄存器2
  #define SD3031_REG_CTR3          0x11  ///< 控制寄存器3
  #define SD3031_REG_COUNTDOWM     0X13  ///< 倒计时寄存器
  #define SD3031_REG_TEMP          0x16  ///< 内部温度寄存器
   #define SD3031_REG_IIC_CON      0x17  ///< IIC控制
  #define SD3031_REG_BAT_VAL       0x1A  ///< 电池电量

public:
  /**
   * @enum  eHours_t
   * @brief  e24hours, e12hours
   */
  typedef enum{
    e24hours = 0,
    e12hours = 1
  }eHours_t;

  /**
   * @enum eWeek_t
   * @brief 星期枚举定义
   */
  typedef enum{
    eSunday    = 0x01,
    eMonday    = 0x02,
    eTuesday   = 0x04,
    eWednesday = 0x08,
    eThursday  = 0x10,
    eFriday    = 0x20,
    eSaturday  = 0x40,
    eEveryDay  = 0x7f,
    eWorkday   = 0x3e,
  }eWeek_t;


  /**
   * @enum  eTrigger_t
   * @brief  中断定义枚举
   */
  typedef enum{
    eYearEnable = 0x40,                    
    eMondayEnable = 0x20,                   
    eDayEnable = 0x10,            
    eHoursEnable = 0x04,       
    eMinuteEnable = 0x02,
    eSecondEnable =0x01,
  }eTrigger_t;

  /**
   * @fn DFRobot_SD3031
   * @brief Constructor
   * @param pWire Wire address
   * @return None
   */
  DFRobot_SD3031(TwoWire *pWire = &Wire){_pWire = pWire;};

  /**
   * @fn begin
   * @brief 初始化传感器
   * @return 返回初始化状态
   */
  uint8_t begin(void);

  /**
   * @fn getRTCTime
   * @brief 获取时钟模块中的年
   * @return 返回获取的年份
   */
  sTimeData_t getRTCTime(void);

  /**
   * @brief 设置时钟是24小时制还是12小时制
   * @param mode 时钟计算方式
   */
  void setHourSystem(eHours_t mode){ _mode = mode; };

  /**
   * @fn setTime
   * @brief Set time into rtc and take effect immediately
   * @param year 2000~2099
   * @param month 1~12
   * @param day 1~31
   * @param week 0~6
   * @param hour 0~23
   * @param minute 0~59
   * @param second 0~59
   * @return None
   */
  void setTime(uint16_t year, uint8_t month, uint8_t day,uint8_t hour, uint8_t minute, uint8_t second);


  /**
   * @fn setAlarm
   * @brief 设置触发报警的数据
   * @param year 2000~2099
   * @param month 1~12
   * @param day 1~31
   * @return None
   */
  void setAlarm(uint16_t year, uint8_t month, uint8_t day);
  /**
   * @fn setAlarm
   * @brief Set the Alarmnumber object
   * @param week 
   * @n ---------------------------------------------------------------------------------------------------------
   * @n |    bit7    |    bit6    |    bit5    |    bit4    |    bit3    |    bit2    |    bit1    |    bit0    |
   * @n ---------------------------------------------------------------------------------------------------------
   * @n |            |  Saturday  |  Friday    |  Thursday  | Wednesday  |  Tuesday   |  Monday    |  Sunday    |
   * @n ---------------------------------------------------------------------------------------------------------                  
   * @param hour 0~23
   * @param minute 0~59
   * @param second 0~59
   */
  void setAlarm(uint8_t week,uint8_t hour, uint8_t minute, uint8_t second);

  /**
   * @brief 获取时钟内部温度
   * @return 返回获取得温度，单位：℃
   */
  int8_t getTemperatureC(void);

  /**
   * @brief 获取板载电池电压
   * @return float 返回获取得电压
   */
  float getVoltage(void);

  /**
   * @brief 清除报警标志位
   */
  void clearAlarm(void);

  /**
   * @fn getAMorPM
   * @brief output AM or PM of time
   * @return AM or PM, 24 hours mode return empty string
   */
  String getAMorPM();

  /**
   * @fn enable32k
   * @brief enable the 32k output 
   * @return None
   */
  void enable32k();

  /**
   * @fn disable32k
   * @brief disable the 32k output
   * @return None
   */
  void disable32k();

  /**
   * @fn writeSRAM
   * @brief write the SRAM
   * @param addr 0x2c~0x0x71
   * @param data uint8_t HEX
   * @return true means write is successful, false means write is failed
   */
  uint8_t writeSRAM(uint8_t addr, uint8_t data);

  /**
   * @fn readSRAM
   * @brief readthe SRAM
   * @param addr 0x2c~0x0x71
   * @return data store in the SRAM
   */
  uint8_t readSRAM(uint8_t addr);

  /**
   * @fn clearSRAM
   * @brief clear the SRAM
   * @param addr 0x2c~0x0x71
   * @return true means clear is successful, false means clear is failed
   */
  uint8_t clearSRAM(uint8_t addr);
  
  /**
   * @fn countDown
   * @brief 倒计时
   * @param second  倒计时时间 0~0xffffff
   */
  void countDown(uint32_t second);

private:
  TwoWire *_pWire;
  eHours_t _mode = e24hours;
  uint8_t _deviceAddr = SD3031_IIC_ADDRESS;

  /**
   * @fn writeReg
   * @brief 写寄存器函数，设计为虚函数，由派生类实现函数体
   * @param reg  寄存器地址 8bits
   * @param pBuf 要写入数据的存放缓存
   * @param size 要写入数据的长度
   * @return None
   */
  uint8_t writeReg(uint8_t reg, void* pBuf, size_t size);

  /**
   * @fn readReg
   * @brief 读取寄存器函数，设计为虚函数，由派生类实现函数体
   * @param reg  寄存器地址 8bits
   * @param pBuf 要写入数据的存放缓存
   * @param size 要写入数据的长度
   * @return uint8_t类型,表示读寄存器状态返回
   * @retval 0 读取成功
   * @retval 1 读取失败
   */
  uint8_t readReg(uint8_t reg, void* pBuf, size_t size);

  /**
   * @fn bcd2bin(uint8_t val)
   * @brief BCD code to BIN code
   * @param val Input BCD code
   * @return Return BIN code
   */
 uint8_t bcd2bin(uint8_t val);

  /**
   * @fn bin2bcd(uint8_t val)
   * @brief BIN code to BCD code
   * @param val Input BIN code
   * @return Return BCD code
   */
  uint8_t bin2bcd(uint8_t val);

};
#endif
