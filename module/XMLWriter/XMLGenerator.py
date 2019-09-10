import os
import sys
import copy

import xml.etree.cElementTree as ET


def xml_writer(obj_dict_all, xml_bs_pth, stock_num):
    for obj_key in obj_dict_all.keys():
        obj_dict = obj_dict_all[obj_key]

        statement = ET.Element("statement")
        for date in obj_dict.keys():
            obj_per_date = obj_dict[date]
            obj_temp = ET.SubElement(statement,"t{}".format(date))
            for item in obj_per_date.keys():
                obj_per_date_item_value = obj_per_date[item]
                ET.SubElement(obj_temp, "{}".format(item)).text = obj_per_date_item_value

        tree = ET.ElementTree(statement)
        tree.write('{}/{}/{}.xml'.format(xml_bs_pth, stock_num, obj_key))

