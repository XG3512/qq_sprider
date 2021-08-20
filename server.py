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


url = 'http://127.0.0.1:8081/'
data = {'recognize_img': img_str, 'type': '0', 'useAntiSpoofing': '0'}
json_mod = json.dumps (data)
res = requests.post (url=url, data=json_mod)
print (res.text)
# 如果服务器没有报错，传回json格式数据
print (eval (res.text))