# !usr/bin/python
# -*- coding: utf-8 -*-


import json
import xlwt

music_list = []
sheet_list = []
json_file = raw_input("Please input the json file name:")
f = open(json_file)
for line in f.readlines():
    music_list.append(json.loads(line))
for item in music_list:
    list_name = item['list_name']
    if list_name not in sheet_list:
        sheet_list.append(list_name)
style = xlwt.easyxf(u'align: wrap on, vert center, horiz center')
title = xlwt.easyxf(u'font:name 宋体, height 200, colour_index black, bold on, italic off; align: wrap on, vert center, horiz center; pattern: pattern solid, fore_colour light_orange;')
workbook = xlwt.Workbook(encoding='utf-8')
for sheet_name in sheet_list:
    sheet = workbook.add_sheet(sheet_name, cell_overwrite_ok=True)
    sheet.write(0, 0, u'排名', title)
    sheet.write(0, 1, u'歌名', title)
    sheet.write(0, 2, u'歌手', title)
    for item in music_list:
        if item['list_name'] == sheet_name:
            sheet.write(item['num'], 0, item['num'], style)
            sheet.write(item['num'], 1, item['song'], style)
            sheet.write(item['num'], 2, item['singer'], style)
workbook.save(u'音乐排行榜.xls')
raw_input("Done! Enter to Exit.")