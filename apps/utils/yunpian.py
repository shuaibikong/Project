import requests
import json


class YunPian:

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            #短信格式
            "text": "【慕学生鲜】您的验证码是{code}。如非本人操作，请忽略此短信".format(code=code),
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.load(response.text)
        return re_dict