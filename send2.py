import requests
import json
import base64
import socket


# 首先将图片读入
# 由于要发送json，所以需要对byte进行str解码
def getByte(path):
    with open (path, 'rb') as f:
        img_byte = base64.b64encode (f.read ())
    img_str = img_byte.decode ('ascii')
    return img_str


img_str = getByte ('a.jpg')


# 此段为获得ip，本人使用本机服务器测试
def getIp():
    try:
        s = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
        s.connect (('127.0.0.1', 80))
        ip = s.getsockname () [0]
    finally:
        s.close ()
    return ip


url = 'http://' + str (getIp ()) + ':9888/'
data = {'recognize_img': img_str, 'type': '0', 'useAntiSpoofing': '0'}
json_mod = json.dumps (data)
res = requests.post (url=url, data=json_mod)
print (res.text)
# 如果服务器没有报错，传回json格式数据
print (eval (res.text))