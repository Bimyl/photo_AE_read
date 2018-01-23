#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Bimyl
# @Date:   2017-11-30 12:02:26
# @Last Modified by:   Bimyl
# @Last Modified time: 2017-12-13 11:38:40
import os
import xlwt
import exifread
from PIL import Image


def gray_average(file):
    # calculation  the image brightness
    i = Image.open(file)
    pixels = i.load()  # this is not a list, nor is it list()'able
    width, height = i.size
    R = 0
    G = 0
    B = 0
    n = 1
    for x in range(1500, 2200):
        for y in range(900, 1200):
            cpixel = pixels[x, y]
            R += (cpixel[0] - R) / n * 1.0
            G += (cpixel[1] - G) / n * 1.0
            B += (cpixel[2] - B) / n * 1.0

# an RGB to brightness formula
            avg_out = (0.3 * R + 0.59 * G + 0.11 * B)
            n += 1
    return int(avg_out)


def file_name(file_dir):
    # Traverse all the image file
    l = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                l.append(os.path.join(root, file))
    return l


def ae_exif(f, i, name):
    # Traverse all the exif information and write to the excel
    tags = exifread.process_file(f, details=False, strict=True)
    tag = {}
    print("%s" % name[2:-4:])
    sheet.write(i + 1, 0, float(name[2:-4:]))

    for key, value in tags.items():
        if key in ('EXIF ExposureTime'):
            tag[key] = str(value)
            print ("%s == %s" % (key, value))
            sheet.write(i + 1, 1, tag[key])
        elif key in ('EXIF ISOSpeedRatings'):
            tag[key] = str(value)
            print ("%s == %s" % (key, value))
            sheet.write(i + 1, 2, int(tag[key]))


def main():
    global sheet, i, index
# init excel information
    data = xlwt.Workbook(encoding='ascii')
    sheet = data.add_sheet("AE")
    sheet.write(0, 0, "LV")
    sheet.write(0, 1, "shutter")
    sheet.write(0, 2, "gain")
    sheet.write(0, 3, "brightness")
    i = 0
    for index in file_name('.'):
        name = index
        f = open(name, 'rb')
        ae_exif(f, i, name)
        gray_brightness = gray_average(name)
        sheet.write(i + 1, 3, gray_brightness)
        print("brightness == %s" % (gray_brightness))
        i = i + 1
    data.save('ae.xls')


if __name__ == '__main__':
    main()
