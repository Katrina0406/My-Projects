import requests
import time
import hashlib
import hmac
import base64
import re

from django.shortcuts import render, HttpResponse

def SendMessage(secret_key, token, message = ''):

    # secret：密钥，机器人安全设置页面，加签一栏下面显示的SEC开头的字符串，例如：SECxxxxxxxx
    # 'SEC4663511a4be8186fb56915a9cdc184c8d6dd6d9fdc757a4f07a210ed4bf11670'
    secret = secret_key
    # access_token：创建完钉钉机器人之后会自动生成，例如：access_tokenxxxx
    # '06a52ec5150109152dbc46a6c1ecc5db8fe1b8484be50f4ad2447700be21cece'
    access_token = token
    # timestamp：当前时间戳，单位是毫秒，与请求调用时间误差不能超过1小时
    timestamp = int(round(time.time() * 1000))

    # 加密，获取sign和timestamp
    data = (str(timestamp) + '\n' + secret).encode('utf-8')
    secret = secret.encode('utf-8')
    signature = base64.b64encode(hmac.new(secret, data, digestmod=hashlib.sha256).digest())
    reg = re.compile(r"'(.*)'")
    signature = str(re.findall(reg,str(signature))[0])

    # 发送信息
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s&sign=%s&timestamp=%s' % (access_token,signature,timestamp)
    headers = {"Content-Type": "application/json ;charset=utf-8 "}
    try:
        response = requests.post(url, headers = headers, json = message, timeout = (3,60))
        print(response)
        response_msg = str(response.status_code) + ' ' + str(response.content)
        print(response_msg)
    except Exception as error_msg:
        print('error_msg==='+str(error_msg))
        response_msg = error_msg

    return response_msg

def sendDD(request):
    if request.method == "POST":
        secret = request.POST.get('secret')
        token = request.POST.get('token')
        content = request.POST.get('content')
        user_mobiles = request.POST.get('user_mobiles')
        user_mobiles = user_mobiles.replace(" ", "")
        users = user_mobiles.split(',')
        isatall = request.POST.get('isatall')
        if isatall == 'False':
            atAll = False
        elif isatall == 'True':
            atAll = True
        msg = {
            "msgtype":"text",
            "text":{"content":content},
            "at": {
                "atMobiles": users,
                "isAtAll": atAll
            }
        }
        try:
            SendMessage(secret, token, msg)
            return HttpResponse('message successfully sent to DingDing!')
        except:
            return HttpResponse('failed to send:(')
    return render(request, "ding.html")



# if __name__ == "__main__":
#     msg = {
#     "msgtype":"text",
#     "text":{"content":"*预报：今天是星期三：）"},
#     "at": {
#           "atMobiles": [
#               "15650799296"
#           ],
#           "isAtAll": False
#       }
#     }
    
    # msg = {
    #  "msgtype": "markdown",
    #  "markdown": {
    #      "title":"杭州天气",
    #      "text": "#### 杭州天气 @150XXXXXXXX \n> 9度，西北风1级，空气良89，相对温度73%\n> ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)\n> ###### 10点20分发布 [天气](https://www.dingalk.com) \n"
    #  },
    #   "at": {
    #       "atMobiles": [
    #           "15650799296"
    #       ],
    #       "isAtAll": False
    #   }
    #     }
 
    # SendMessage(msg)