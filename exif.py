#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Bimyl
# @Date:   2017-11-30 12:02:26
# @Last Modified by:   Bimyl
# @Last Modified time: 2017-12-06 18:05:04
import os
import xlwt
import exifread


def file_name(file_dir):
    l = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                l.append(os.path.join(root, file))
    return l


data = xlwt.Workbook(encoding='ascii')
sheet = data.add_sheet("AE")

i = 0
for index in file_name('.'):
    name = index
    f = open(name, 'rb')
    tags = exifread.process_file(f, details=False, strict=True)
    tag = {}
    print("%s" % name)
    sheet.write(i, 0, name[2:])

    for key, value in tags.items():
        if key in ('EXIF ExposureTime'):
            tag[key] = str(value)
            print ("%s == %s" % (key, value))
            sheet.write(i, 1, tag[key])
        elif key in ('EXIF ISOSpeedRatings'):
            tag[key] = str(value)
            print ("%s == %s" % (key, value))
            sheet.write(i, 2, tag[key])
    i = i + 1

data.save('ae.xls')
