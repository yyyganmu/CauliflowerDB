#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: YANG Yuyao
# time: 2023-02-24
# check the line separator

from django.conf import settings
import hashlib


def md5(string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(string.encode('utf-8'))
    return obj.hexdigest()