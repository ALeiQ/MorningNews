#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" 早报抓取 """

__author__ = 'Haso'

import html
import time
from urllib import request
from sendEmail import send_email
import re
import logging


#logging.basicConfig(filename='LOG/'+__name__+'.log',
#                    format='[%(asctime)s-%(filename)s-%(levelname)s: %(message)s]',
#                    level = logging.DEBUG,
#                    filemode='a',
#                    datefmt='%Y-%m-%d %I:%M:%S %p')

main_web = 'http://www.pmtown.com/archives/category/%E6%97%A9%E6%8A%A5'


def get_morning(type = '分钟'):
    logging.info('Start catching......')
    receive_emails = []

    with open('receive_emails', 'r') as f:
        for x in f.readlines():
            x = solve_email(x)
            if x:
                receive_emails.append(x)

    web_html = get_html(main_web)
    items = get_items(web_html)
    link_dates = get_link_dates(items)

    new_link = link_dates[0]
    if type in new_link.date:
        new_html = get_html(new_link.url)
        title, message = get_message(new_html)
        em = send_email(title, message, receive_emails)
        em.do_send()
        logging.info('早报任务执行完成')
        return True
    else:
        logging.warning('未抓取到早报，10分钟后重试')
        return False


def solve_email(email):
    email = email.strip()
    if email.startswith('#'):
        email = None
    return email


def get_html(url):
    page = request.urlopen(url)
    html = page.read()
    return html.decode('UTF-8')


def get_items(html):
    reg = '<li class="item">(.*?)</li>'
    page = re.compile(reg, re.S)

    artlist = page.findall(html)

    return artlist


def get_link_dates(items):
    reg = '<a href="(.*?)" title='
    date_reg = '<span class="item-meta-li date">(.*?)</span>'
    page = re.compile(reg, re.S)
    page_date = re.compile(date_reg, re.S)

    link_dates = []

    try:
        for item in items:
            link_dates.append(link_date(page.findall(item)[0],
                              page_date.findall(item)[0]))
    except Exception as ex:
        logging.error('网页数据解析异常: ' + ex)

    return link_dates


def get_message(url):
    reg = '<article.*?>(.*?)</article>'
    page = re.compile(reg, re.S)
    article = page.findall(url)[0]

    h1 = '<h1.*?>[\n]?(.*?)</h1>'
    page = re.compile(h1, re.S)
    main_page = page.findall(article)

    other_reg = '<div class="entry-footer"(.*)'
    page = re.compile(other_reg, re.S)
    article = page.sub('', article)

    img_reg = '<img(.*?)>'
    page = re.compile(img_reg, re.S)
    article = page.sub('', article)

    link_reg = '(<a(.*?)>)|(</a>)'
    page = re.compile(link_reg, re.S)
    article = page.sub('', article)

    return html.unescape(main_page[0]), article


class link_date(object):
    def __init__(self, url, date):
        self.url = url
        self.date = date

    def write_console(self):
        print(self.link, self.date)

if __name__ == '__main__':
    get_morning('小时')

