#! encoding:utf-8
import requests
import base64
import json
import time
import hashlib
from Crypto.Cipher import AES

appid = '8097033776455989'
appsecret = '829dfd1f2eb24beda20f5fe65c786416'
# http_domain = 'http://openuat.ersoft.cn'
http_domain = 'http://192.168.0.9:8079'


class SsoInterface(object):

    def decrypt(self, encrypt, token):
        cipher = AES.new(token)
        b = base64.b64decode(encrypt)
        return cipher.decrypt(b)
    
    def oauth2_token(self):
        url = http_domain + '/api/oauth2/oauth2_token'
        headers = {'appid': appid, 'timestamp': int(time.time())}
        headers = {'identification': base64.b64encode(json.dumps(headers))}
        response = requests.post(url=url, headers=headers)
        print response.json()
        return response

    def access_token(self, linkid, token):
        url = http_domain + '/api/oauth2/access_token'
        # 获取加密的appsecret
        sh = hashlib.sha256()
        sh.update(appsecret)
        body = json.dumps({
            'appsecret': sh.hexdigest(),
            'appid': appid,
        })
        print 'body is %s' % body

        # 加密body
        cipher = AES.new(token)
        BS = AES.block_size
        source = body + (BS - len(body) % BS) * ' '
        encrypt_body = cipher.encrypt(source)
        b64_encry_body = base64.b64encode(encrypt_body)
        
        # 获取摘要
        m1 = hashlib.md5()
        m1.update(b64_encry_body)
        m2 = hashlib.md5()
        sign = m1.hexdigest() + token + appid
        m2.update(sign.encode('utf-8'))
        data = {
            'data': b64_encry_body,
            'summary': m2.hexdigest(),
        }

        # 获取headers
        headers = {'linkid': linkid, 'timestamp': int(time.time())}
        headers = {'identification': base64.b64encode(json.dumps(headers))}
        print 'request body is %s' % body
        print 'request headers is %s' % headers

        # post
        response = requests.post(url=url, data=data, headers=headers)
        print response.json()
        print self.decrypt(response.json().get('data'), token)
        return response

if __name__ == '__main__':
    sso = SsoInterface()
    oauth2_token_response = sso.oauth2_token()
    oauth2_token = oauth2_token_response.json()
    access_token = sso.access_token(oauth2_token.get('data').get('linkid'), oauth2_token.get('data').get('token'))


