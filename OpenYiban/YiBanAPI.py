from .Config import config
import requests
import json

CODE_URI = config.base_url+"oauth/authorize?client_id="+config.client_id+"&redirect_uri="+config.redirect_uri

def get_access_token_and_user_id(code):
    data = {
        'client_id':(None,config.client_id),
        'client_secret':(None,config.client_secret),
        'code':(None,code),
        'redirect_uri':(None,config.redirect_uri)
    }
    response = requests.request("POST", config.base_url+'oauth/access_token', data=data)
    response = json.loads(response.text)
    token = response.get('access_token', '0')
    user_id = response.get('userid', '0')
    return token,user_id

def get_token_info(access_token='',yb_uid=''):
    data = {
        'client_id':(None,config.client_id),
        'access_token':(None,access_token),
        'yb_uid':(None,yb_uid)
    }
    response = requests.request("POST", config.base_url+'oauth/token_info', data=data)
    response = json.loads(response.text)
    status = response.get('status', 'error')
    expire_in = response.get('expire_in', -1)
    return status,expire_in

def get_user_info(access_token):
    data = {"access_token": access_token}
    info = {'userid':'','username':'','usernick':'','sex':'','schoolname':''}
    response = requests.request("GET", config.base_url+'user/me', params=data)
    response = json.loads(response.text)
    if 'success' != response.get('status', 'error'):
        return 'error'
    info_data = response.get('info')
    info['userid'] = info_data['yb_userid']
    info['username'] = info_data['yb_username']
    info['usernick'] = info_data['yb_usernick']
    info['schoolname'] = info_data['yb_schoolname']
    if 'M' == info_data['yb_sex']:
        info['sex'] = '男'
    elif 'F' == info_data['yb_sex']:
        info['sex'] = '女'
    else:
        info['sex'] = '未知'
    return info

def revoke_token(access_token):
    data = {
        'client_id': (None, config.client_id),
        'access_token':(None,access_token)
    }
    response = requests.request("POST", config.base_url + 'oauth/revoke_token', data=data)
    response = json.loads(response.text)
    if '200' == response.get('status', 'error'):
        return '200'
    else:
        return 'error!'