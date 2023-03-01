import json
from io import BytesIO
from typing import Tuple

import requests
import pandas as pd
import configparser
from pyDes import des, CBC, PAD_PKCS5
import binascii
import base64

password = 0xB9
read_ini = configparser.ConfigParser()

'''
获取配置文件，没啥用
'''


def getIni():
    return getByteStream("http://002001a.oss-accelerate.aliyuncs.com/a/a.txt")


def getByteStream(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            response_byte = response.content
            bytes_stream = BytesIO(response_byte)
            byteList = bytearray()
            num = bytes_stream.read()
            for n in num:
                byteList.append(n ^ password)

            result = byteList.decode("gb2312")
        else:
            result = response
    except Exception:
        result = '<Response [404]>'
    return result


table_header = ['编号', '密码', "中文名", '英文名', '详情', '下载地址1', '下载地址2']


def GetContentList():
    url = "http://42.51.180.71:5000/API/APIUnified/"
    body = {'Action': 'GetContentList'}
    headers = {'content-type': "application/x-www-form-urlencoded"}
    session = requests.session()
    response = session.post(url, data=body, headers=headers, verify=False)

    if response.status_code == 200:
        response_content = response.content.decode(encoding='UTF-8', errors='strict')
        response_json = json.loads(response_content)
        data = response_json['Data']

        list = []
        idx = 0
        for row in data:
            tmp_list = []
            idx = idx + 1
            # Id = DecryptDES(str(row['Id']))
            BH = DecryptDES(row['BH']).decode("utf-8")
            MM = DecryptDES(row['MM']).decode("utf-8")
            Name1 = DecryptDES(row['Name1']).decode("utf-8")
            Name2 = DecryptDES(row['Name2']).decode("utf-8")

            tmp_list.append(BH)
            tmp_list.append(MM)
            tmp_list.append(Name1)
            tmp_list.append(Name2)

            try:
                info, xiazai1, xiazai2 = getGameDownLoadURL(BH)
            except:
                info = ''
                xiazai1 = ''
                xiazai2 = ''
            tmp_list.append(info)
            tmp_list.append(xiazai1)
            tmp_list.append(xiazai2)
            print(tmp_list)
            list.append(tmp_list)

        df = pd.DataFrame(columns=table_header, data=list)
        df.to_csv('./data/Games.csv', encoding='utf-8', index=None)
        df.to_excel('./data/Games.xlsx', sheet_name='sheet_1', index=False)

    else:
        print(response)


'''
没啥用
'''


def GetMoreContentList():
    url = "http://42.51.180.71:5000/API/APIUnified/"
    body = {'Action': 'GetMoreContentList'}
    headers = {'content-type': "application/x-www-form-urlencoded"}
    session = requests.session()
    response = session.post(url, data=body, headers=headers, verify=False)

    if response.status_code == 200:
        response_content = response.content.decode(encoding='UTF-8', errors='strict')
        response_json = json.loads(response_content)
        data = response_json['Data']

        for i in data:
            BiaoQ = DecryptDES(i['BiaoQ'])
            XingJ = DecryptDES(i['XingJ'])
            MageA = DecryptDES(i['MageA'])
            RongL = DecryptDES(i['RongL'])
            RiQ = DecryptDES(i['RiQ'])
            Category = DecryptDES(i['Category'])
            i['BiaoQ'] = BiaoQ.decode("utf-8")
            i['XingJ'] = XingJ.decode("utf-8")
            i['MageA'] = MageA.decode("utf-8")
            i['RongL'] = RongL.decode("utf-8")
            i['RiQ'] = RiQ.decode("utf-8")
            i['Category'] = Category.decode("utf-8")
            print(i, end="\n")

    else:
        print(response)


def DecryptDES(input) -> str:
    secret_key = 'consmkey'
    iv = [18, 52, 86, 120, 144, 171, 205, 239]
    des_obj = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)

    return des_obj.decrypt(base64.b64decode(input))


def getGameDownLoadURL(BH) :
    url = "http://002001a.oss-accelerate.aliyuncs.com/c/" + str(BH) + ".txt"
    ini_str = getByteStream(url)
    if '<Response [404]>' in ini_str or '<Response [502]>' in ini_str or len(ini_str) == 0:
        print(ini_str + ' for ' + BH)
        return '<Response [404]>', '<Response [404]>', '<Response [404]>'

    ini_str.replace('(', ' ')
    try:
        read_ini.read_string(ini_str)
    except Exception:
        return '<Response [404]>', '<Response [404]>', '<Response [404]>'

    try:
        info = read_ini['zhu']['yxbb']
    except Exception:
        info = ''
    try:
        xiazai1 = read_ini['xiazai']['xiazai1_dizhi']
    except Exception:
        xiazai1 = ''

    try:
        xiazai2 = read_ini['xiazai']['xiazai2_dizhi']
    except Exception:
        xiazai2 = ''

    return info, xiazai1, xiazai2


if __name__ == '__main__':
    GetContentList()
