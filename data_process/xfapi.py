#此为讯飞api的测试脚本
#coding=utf-8

import time 
import urllib.request
import urllib.parse
import json
import hashlib
import base64

url_parse = 'http://ltpapi.xfyun.cn/v1/sdp'
url_cut = 'http://ltpapi.xfyun.cn/v1/cws'
appid = '5cc4f597'
appid_key = 'ab973c475672862ad887ee93c5d3a81e'

content=''

def main(sentence):
        body = urllib.parse.urlencode({'text':sentence}).encode('utf-8')
        param = {'type':'dependent'}
        x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
        x_time = str(int(time.time()))
        x_chencksum = hashlib.md5(appid_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
        x_header = {
            'X-Appid':appid,
            'X-CurTime':x_time,
            'X-Param':x_param,
            'X-CheckSum':x_chencksum}
        req_parse = urllib.request.Request(url_parse, body, x_header)
        req_cut = urllib.request.Request(url_cut, body, x_header)
        result_parse = urllib.request.urlopen(req_parse)
        result_cut = urllib.request.urlopen(req_cut)
        result_parse = result_parse.read()
        result_cut = result_cut.read()
        print(result_cut.decode('utf-8'))
        print(result_parse.decode('utf-8'))


while True:
    content=input('please input the sentence:')
    main(content)


    