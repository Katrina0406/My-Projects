import requests
import json
import sys
import importlib

importlib.reload(sys)
requests.packages.urllib3.disable_warnings()

from django.shortcuts import render, HttpResponse

class WeChat:

    def __init__(self, corpid, corpsecret, agentid, userid):

        self.CORPID = corpid
        self.CORPSECRET = corpsecret
        self.AGENTID = agentid
        self.TOUSER = userid # 接收者用户名

    def _get_access_token(self):

        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
        'corpsecret': self.CORPSECRET,
        }
        req = requests.post(url, params=values, verify=False)

        return req

    def get_access_token(self):

        get_req = self._get_access_token()
        if get_req.status_code != 200:
            print('连接服务器失败')
        else:
            get_req_json = json.loads(get_req.text)
        if get_req_json['errcode'] != 0:
            print('响应结果不正确')
        else:
            access_token = get_req_json['access_token']

        return access_token

    def send_data(self, message):

        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()

        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
            "content": message
            },
            "safe": "0"
        }

        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges, verify=False)
        respone = respone.json()

        return respone["errmsg"]

def runMsg(request):
    # corpid = 'ww3125334d3d987bfb'
    # corpsecret = 'DmdjkVc59NAwk5tta-0ckZIsMFdPeaOZzfZpkHTQ6ao'
    # agentid = '1000011'
    # userid = "HuYuQiao"
    if request.method == "POST":
        corpid = request.POST.get('corpid')
        corpsecret = request.POST.get('corpsecret')
        agentid = request.POST.get('agentid')
        userid = request.POST.get('userid')
        content = request.POST.get('content')
        try:
            wx = WeChat(corpid, corpsecret, agentid, userid)
            wx.send_data(content)
            return HttpResponse('message successfully sent to Wechat Work!')
        except:
            return HttpResponse('connection to WeChat Work fail:(')
    return render(request, "index.html")
