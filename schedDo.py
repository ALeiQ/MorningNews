#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" 定时任务 """

__author__ = 'Haso'

import getMorning
import sched, time

import logging


logging.basicConfig(filename='LOG/logging.log',
                    format='[%(asctime)s-%(filename)s-%(levelname)s: %(message)s]',
                    level = logging.DEBUG,
                    filemode='a')

scd = sched.scheduler(time.time, time.sleep)
counter = 0


def main():
    #scd.enter(0, 1, echo_test_msg, ())
    #scd.enterabs(each_day_time(17, 38, 0, False), 1, echo_test_msg, ())
    scd.enterabs(each_day_time(8, 20, 0, False), 1, echo_test_msg, ())
    scd.run()


def each_day_time(hour, min, sec, next_day=True):
    struct = time.localtime()
    if next_day:
        day = struct.tm_mday + 1
    else:
        day = struct.tm_mday
    return time.mktime((struct.tm_year, struct.tm_mon, day, hour, min, sec, struct.tm_wday,
                        struct.tm_yday, struct.tm_isdst))


def echo_test_msg():
    scd.enterabs(each_day_time(8, 20, 0, True), 1, echo_test_msg, ())
    circle_catch()


def circle_catch():
    global counter
    counter += 1
    # 每隔10分钟抓取一次，超过12次则取消
    if getMorning.get_morning():
        counter = 0
    elif counter == 12:
        logging.warning('两小时仍未抓到，当日无早报！！')
        counter = 0
    else:
        #scd.enter(1, 0, circle_catch, ())
        scd.enter(10*60, 0, circle_catch, ())



main()
