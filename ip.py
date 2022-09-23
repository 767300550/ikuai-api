import hashlib
import base64
from http.cookiejar import Cookie
import requests
import json


def ip_hs(url, cokie, username):
    print(url + cokie)
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': url,
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }

    cookie = {
        'sess_key': cokie,
        'useradmin': username,
        'login': '1'
    }
    print(cookie)
    json_data = {
        'func_name': 'dhcp_lease',
        'action': 'recycle',
        'params': {},
    }
    req = requests.post(url + "/Action/call", cookies=cookie,
                        json=json_data, headers=headers, verify=False)
    print(req.text)


def get_cookie(url, username, password):
    password_md5 = hashlib.md5(password.encode()).hexdigest()
    passwd = "salt_11" + password
    password_b64 = str(base64.b64encode(passwd.encode("UTF-8")), "UTF-8")
    data = {
        "username": username,
        "passwd": password_md5,
        "pass": password_b64,
        "remeber_password": "true"
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': url,
        'Referer': url + "/login",
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', }

    res = requests.post(url + "/Action/login", json=data,
                        headers=headers, verify=False)
    print(res.text)
    cookie = requests.utils.dict_from_cookiejar(res.cookies)
    cokkie = cookie['sess_key']
    ip_hs(url, cokkie, username)


if __name__ == '__main__':
    url = ""
    username = "admin"
    password = ""
    get_cookie(url, username, password)
