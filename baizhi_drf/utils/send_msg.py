import requests


class SMSSend(object):
    def __init__(self,api_key):
        self.api_key =api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_msg(self,phone,code):
        params={
            'apikey':self.api_key,
            'mobile':phone,
            'text':"【杨锐test】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        re=requests.post(self.single_send_url,data=params)
        print(re)
# if __name__ == '__main__':
#      sms=SMSSend('40d6180426417bfc57d0744a362dc108')
#      sms.send_msg('15633089786','123qwe')