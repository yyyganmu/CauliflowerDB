#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: YANG Yuyao
# time: 2024/4/8
# check the line separator
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

import pymysql as pm
from tqdm import tqdm


def insert_data():
    user = 'root'
    host = 'taascr.myddns.me'
    port = 7252
    db = 'webdata'
    password = 'Yy374521.'

    file = input('Enter the sample info file: ')
    with open(file, 'r') as fi:
        lll = [line.strip().split('\t') for line in fi.readlines()]
        lll = sorted(lll, key=lambda x: x[0], reverse=False)

    connection = pm.connect(host=host, user=user, password=password, port=port, db=db)
    cursor = connection.cursor()
    print('DATABASE CONNECTED')

    cursor.execute("TRUNCATE TABLE `sampleinfo`;")
    connection.commit()
    print('TABLE TRUNCATED')

    for ll in tqdm(lll):
        sql = f"INSERT INTO `sampleinfo` VALUES ('{ll[0]}', '{ll[1]}', '{ll[2]}', '{ll[3]}', '{ll[4]}');"
        cursor.execute(sql)
    connection.commit()
    print('INSRTION COMPLETE')


if __name__ == '__main__':
    insert_data()