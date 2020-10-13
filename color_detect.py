#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import sys
import MySQLdb
from MySQLdb.cursors import DictCursor
from datetime import datetime
import hashlib
import db_connect
import cv2
import numpy as np


# 引数取得
argvs = sys.argv
print(f'引数：{argvs}')

#img = cv2.imread(argvs[1])
#img = cv2.blur(img, ksize=(3,3))
img = cv2.imread("test.jpeg")
img = cv2.blur(img, ksize=(3,3))

# ファイル名文字列からDB用timestamp文字列の作成
tdatetime  = datetime.strptime(argvs[1].split('.')[0], '%Y%m%d%H%M')
tstr = tdatetime.strftime('%Y/%m/%d %H:%M:00.000')
print(f'timestamp文字列：{tstr}')

def red_detect(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hsv_min = np.array([0,64,0])
    hsv_max = np.array([30,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    hsv_min = np.array([150,64,0])
    hsv_max = np.array([179,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

    mask = mask1 + mask2
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img


def green_detect(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_min = np.array([30,64,0])
    hsv_max = np.array([90,255,255])

    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img


def blue_detect(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_min = np.array([90,64,0])
    hsv_max = np.array([150,255,255])

    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img

red_mask, red_masked_img = red_detect(img)
green_mask, green_masked_img = green_detect(img)
blue_mask, blue_masked_img = blue_detect(img)

point=argvs[3]
conn = db_connect.DatabaseConnect()
cur = conn.cursor(DictCursor)

location=argvs[4]

if np.any(red_mask) != 0:
    print("red mask検出 flag=1")
    #cur.execute("INSERT INTO HSV_MASK_DATA (picture_filename, datetime, picture_code, location_code, r_mask) VALUES (%s, %s, %s, %s, %s) ", (argvs[1], tstr, point, location, tuple(red_masked_img)))
    sql = "INSERT INTO HSV_MASK_DATA (picture_filename, datetime, picture_code, location_code, r_mask) VALUES (%s, %s, %s, %s, %s)"
    val = (argvs[1], tstr, point, location, 1)
    cur.execute(sql, val)
    cur.close()
    conn.commit()
    conn.close()
    #print("masked image array")
    #print(red_masked_img)

elif np.any(green_mask) != 0:
    print("green mask検出 flag=1")
    sql =  "INSERT INTO HSV_MASK_DATA (picture_filename, datetime, picture_code, location_code, g_mask) VALUES (%s, %s, %s, %s, %s)"
    val = (argvs[1], tstr, point, location, 1)
    cur.execute(sql, val)
    cur.close()
    conn.commit()
    conn.close()

elif np.any(blue_mask) != 0:
    print("blue mask検出 flag=1")
    sql = "INSERT INTO HSV_MASK_DATA (picture_filename, datetime, picture_code, location_code, g_mask) VALUES (%s, %s, %s, %s, %s)"
    val = (argvs[1], tstr, point, location, 1)
    cur.execute(sql, val)
    cur.close()
    conn.commit()
    conn.close()
