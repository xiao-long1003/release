# coding:utf-8
import time
import requests
import random
import csv
from urllib import parse
import json
import cv2
import hashlib
from config import path_user, begin_user, end_user


def get_url(user):
    i = user
    user = i[0]
    user = parse.quote(user)
    passw = i[2]
    m = hashlib.md5()
    b = passw.encode(encoding='utf-8')
    m.update(b)
    a_md5 = m.hexdigest()

    url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin"

    payload = "username={}&pwd={}&imgcode=&f=json&userlang=zh_CN&redirect_url=&token=&lang=zh_CN&ajax=1".format(user,
                                                                                                                a_md5)
    headers = {
        'Host': 'mp.weixin.qq.com',
        'Origin': 'https://mp.weixin.qq.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Referer': 'https://mp.weixin.qq.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cookie': 'noticeLoginFlag=1; rewardsn=; wxtokenkey=777; ua_id=KTtQx5LTPMru0MSrAAAAAJVizSrOGRQNwCqVJDvvT0I=; pgv_pvi=5359779840; pgv_si=s9167475712; cert=RPSjZXKEStYjbmA7C1dnL9TVlBwQH57h; noticeLoginFlag=1; mm_lang=zh_CN; tvfe_boss_uuid=31e3bead7132992c; pgv_pvid=9854683648; pgv_info=ssid=s5595119350; uuid=42d90eb28eeea24554c6658befc65406; xid=2a85c7581d6ccb987239a355a4e6084c'
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    cookie = requests.utils.dict_from_cookiejar(response.cookies)
    res = response.text
    res = json.loads(res)
    referer = res['redirect_url']
    # print(cookie)
    bizuin = cookie['bizuin']
    cert = cookie['cert']
    fake_id = cookie['fake_id']
    login_certificate = cookie['login_certificate']
    login_sid_ticket = cookie['login_sid_ticket']
    ticket = cookie['ticket']
    ticket_certificate = cookie['ticket_certificate']
    ticket_id = cookie['ticket_id']
    ticket_uin = cookie['ticket_uin']
    uuid = cookie['uuid']

    a = '''noticeLoginFlag=1; rewardsn=; wxtokenkey=777; ua_id=KTtQx5LTPMru0MSrAAAAAJVizSrOGRQNwCqVJDvvT0I=; pgv_pvi=6856870912; pgv_si=s9167475712; cert={}; noticeLoginFlag=1; mm_lang=zh_CN; tvfe_boss_uuid=31e3bead7132992c; pgv_pvid=9854683648; pgv_info=ssid=s5595119350; xid=1194f32639c6b4b714dc8b47565def4b; uuid={}; bizuin={}; ticket={}; ticket_id={}; ticket_uin={}; login_certificate={}; ticket_certificate={}; fake_id={}; login_sid_ticket={}'''.format(
        cert, uuid, bizuin, ticket, ticket_id, ticket_uin, login_certificate,
        ticket_certificate, fake_id, login_sid_ticket)

    url = "https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=getqrcode&param=4300&rd=821"

    payload = {}
    headers = {
        'Host': 'mp.weixin.qq.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': 'https://mp.weixin.qq.com{}'.format(referer),
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': a,
    }

    requests.packages.urllib3.disable_warnings()
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    name = r'C:\Users\Administrator\Desktop\erweima.jpg'
    img_file = open(name, 'wb')  # 二进制打开文件
    img_file.write(response.content)  # 把图片内容写入文件
    img_file.close()
    time.sleep(1)
    lena = cv2.imread(r'C:\Users\Administrator\Desktop\erweima.jpg')
    cv2.imshow('picture', lena)
    # cv2.waitKey(5)
    # time.sleep(15)
    # cv2.waitKey(1)
    url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login"

    payload = "userlang=zh_CN&redirect_url=&token=&lang=zh_CN&f=json&ajax=1"
    headers = {
        'Host': 'mp.weixin.qq.com',
        'Origin': 'https://mp.weixin.qq.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Referer': 'https://mp.weixin.qq.com{}'.format(referer),
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': a
    }
    while True:
        requests.packages.urllib3.disable_warnings()
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        # print(response.text)
        res = response.text
        res = json.loads(res)
        err_msg = res["base_resp"]["err_msg"]
        if err_msg == 'default':

            print('请使用{}扫码'.format(i[3]))
            cv2.waitKey(1)


        else:
            print('扫码成功')
            break
    cookie_dict = requests.utils.dict_from_cookiejar(response.cookies)
    # print(cookie)
    # print(cookie_dict)
    slave_sid = cookie_dict['slave_sid']
    uuid = cookie['uuid']
    cert = cookie['cert']
    data_ticket = cookie_dict['data_ticket']
    data_bizuin = cookie_dict['data_bizuin']
    slave_user = cookie_dict['slave_user']
    ticket = cookie['ticket']
    ticket_id = cookie['ticket_id']
    pgv_si = 's9167475712'
    pgv_pvi = '6856870912'
    bizuin = cookie_dict['bizuin']
    xid = cookie_dict['xid']
    ua_id = cookie_dict['ua_id']
    noticeLoginFlag = '1'
    mm_lang = cookie_dict['mm_lang']
    List1 = [slave_sid, uuid, cert, data_ticket, data_bizuin, slave_user, ticket, ticket_id, pgv_si, pgv_pvi, bizuin,
             xid, ua_id, noticeLoginFlag, mm_lang]
    List2 = []
    for a in cookie_dict:
        List2.append(a)
    for i in List2:
        if i not in List1:
            n = cookie_dict[i]

            cookie_tup = '''noticeLoginFlag={}; ua_id={} pgv_pvi={}; pgv_si={}; uuid={}; bizuin={}; ticket={}; ticket_id={}; cert={}; data_bizuin={}; data_ticket={}; slave_sid={}; slave_user={}; xid={}; {}={}; mm_lang={}'''.format(
                noticeLoginFlag, ua_id,
                pgv_pvi, pgv_si, uuid, bizuin, ticket, ticket_id, cert, data_bizuin, data_ticket, slave_sid, slave_user,
                xid,
                i, n, mm_lang)
    # print(response.text)
    # {'bizuin': '3570068731', 'data_bizuin': '3570068731', 'data_ticket': 'n8IXzv+0nivL6t8XrklpVcF7xF3RgJ9eJ7xyR34PWYFHN0ybVu/gM78/zSlno2z3', 'mm_lang': 'zh_CN', 'openid2ticket_o--zK1IfT0JjlLi82c4Ob7NfyJb0': '6K4uMmVEyWjzbWpqy8ZZHP3VH0bzP21mwmR877Zptxo=', 'slave_sid': 'MUJZdVBGUEVjUTRnRlUyWEVXU2hJVENyRnlsWUE1N1NkM1lMb0h5Z2taMzlOZE11bnBkRXlBOVhQTlA1MzNmOXU0ajBPaEwwRndhc0ROMnJ0V3lfV0xJb1RRZU5wVjAwdHd2UElaRjFkT2JUUTNieVpxNzRJVDNKdURWdzNISTJlem8yaXRmMnR0cGUwa3pP', 'slave_user': 'gh_00887795e4c9', 'ua_id': 'KTtQx5LTPMru0MSrAAAAAJVizSrOGRQNwCqVJDvvT0I=', 'xid': '9cc33390660e260e4f82fc13261a4431'}
    res = json.loads(response.text)
    redirect = res['redirect_url']
    tooken_url = redirect.split('=')
    tooken = tooken_url[-1]
    return cookie_tup, tooken


def get_appid(tooken, cookie):

    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

    querystring = {"begin": "10", "count": "10", "t": "media/appmsg_list", "type": "10", "action": "list_card",
                   "lang": "zh_CN", "token": tooken, "f": "json"}

    headers = {
        'Host': "mp.weixin.qq.com",
        'Accept': "multipart/form-data",
        'Content-Type': "text/html; charset=utf-8",
        'Cookie': cookie,
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'Accept-Language': "zh-Hans-CN;q=1",
        'Referer': "https://mp.weixin.qq.com/cgi-bin/message/list?count=20&day=7&lang=zh_CN&filterivrmsg=1&token={}".format(
            tooken),
        'cache-control': "no-cache"
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.request("GET", url, headers=headers, params=querystring, verify=False).json()
    # print(response)

    app_msg_info = response['app_msg_info']
    item = app_msg_info['item']
    item7 = item[3]
    app_id = item7['app_id']
    create_time = item7['create_time']
    item6 = item[2]
    app_id1 = item6['app_id']
    create_time1 = item6['create_time']
    return app_id, create_time, app_id1, create_time1


# 发布
def send_data(tooken, cookie, app_id, create_time):
    time1 = str(int(time.time() * 1000))

    url = "https://mp.weixin.qq.com/cgi-bin/masssend"

    querystring = {"action": "get_appmsg_copyright_stat", "token": tooken, "lang": "zh_CN"}

    payload = "ajax=1&appmsgid={}&f=json&first_check=0&lang=zh_CN&random=0.2708198274485767&token={}&type=10".format(
        app_id, tooken)
    headers = {
        'Host': "mp.weixin.qq.com",
        'Accept': "multipart/form-data",
        'Content-Type': "application/x-www-form-urlencoded; charset=utf-8",
        'Cookie': cookie,
        'User-Agent': "WeChatHelper/9.1.9 (iPhone; iOS 13.1.3; Scale/3.00)",
        'Accept-Language': "zh-Hans-CN;q=1",
        'Referer': "https://mp.weixin.qq.com/cgi-bin/masssend?action=get_appmsg_copyright_stat&token={}&lang=zh_CN".format(
            tooken),
        'cache-control': "no-cache"
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False)

    print(response.text)

    url = "https://mp.weixin.qq.com/cgi-bin/masssend"

    querystring = {"action": "get_appmsg_copyright_stat", "token": tooken, "lang": "zh_CN"}

    payload = "ajax=1&appmsgid={}&f=json&first_check=1&lang=zh_CN&random=0.2708198274485767&token={}&type=10".format(
        app_id, tooken)
    headers = {
        'Host': "mp.weixin.qq.com",
        'Accept': "multipart/form-data",
        'Content-Type': "application/x-www-form-urlencoded; charset=utf-8",
        'Cookie': cookie,
        'User-Agent': "WeChatHelper/9.1.9 (iPhone; iOS 13.1.3; Scale/3.00)",
        'Accept-Language': "zh-Hans-CN;q=1",
        'Referer': "https://mp.weixin.qq.com/cgi-bin/masssend?action=get_appmsg_copyright_stat&token={}&lang=zh_CN".format(
            tooken),
        'cache-control': "no-cache",
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False)

    print(response.text)

    url = "https://mp.weixin.qq.com/cgi-bin/masssend"

    querystring = {"t": "ajax-response", "req_need_vidsn": "1", "add_tx_video": "1", "token": tooken, "lang": "zh_CN"}

    payload = "ajax=1&appmsgid={}&cardlimit=1&city=&code=&country=&direct_send=1&f=json&groupid=-1&imgcode=&lang=zh_CN&operation_seq={}&province=&random=0.2708198274485767&req_id=TxOE6Qde9iF2ooOgqZiy2tcOoOcZgIoE&req_time={}&sex=0&synctxweibo=0&token={}&type=10".format(
        app_id, create_time, time1, tooken)
    # print(payload)

    headers = {
        'Host': "mp.weixin.qq.com",
        'Accept': "multipart/form-data",
        'Content-Type': "application/x-www-form-urlencoded; charset=utf-8",
        'Cookie': cookie,
        'User-Agent': "WeChatHelper/9.1.9 (iPhone; iOS 13.1.3; Scale/3.00)",
        'Accept-Language': "zh-Hans-CN;q=1",
        'Referer': "https://mp.weixin.qq.com/cgi-bin/masssendpage?t=mass/send&token={}&lang=zh_CN".format(tooken),
        'cache-control': "no-cache"
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False).json()

    return response


# 预设
def send_time_data(tooken, cookie, app_id1, create_time1, send_time):
    time1 = str(int(time.time() * 1000))

    url = "https://mp.weixin.qq.com/cgi-bin/masssend"

    querystring = {"action": "get_appmsg_copyright_stat", "token": tooken, "lang": "zh_CN"}

    payload = "ajax=1&appmsgid={}&f=json&first_check=0&lang=zh_CN&random=0.2708198274485767&token={}&type=10".format(
        app_id1, tooken)
    headers = {
        'Host': "mp.weixin.qq.com",
        'Accept': "multipart/form-data",
        'Content-Type': "application/x-www-form-urlencoded; charset=utf-8",
        'Cookie': cookie,
        'User-Agent': "WeChatHelper/9.1.9 (iPhone; iOS 13.1.3; Scale/3.00)",
        'Accept-Language': "zh-Hans-CN;q=1",
        'Referer': "https://mp.weixin.qq.com/cgi-bin/masssend?action=get_appmsg_copyright_stat&token={}&lang=zh_CN".format(
            tooken),
        'cache-control': "no-cache"
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False)

    print(response.text)

    url = "https://mp.weixin.qq.com/cgi-bin/masssend"

    querystring = {"action": "get_appmsg_copyright_stat", "token": tooken, "lang": "zh_CN"}

    payload = "ajax=1&appmsgid={}&f=json&first_check=1&lang=zh_CN&random=0.2708198274485767&token={}&type=10".format(
        app_id1, tooken)
    headers = {
        'Host': "mp.weixin.qq.com",
        'Accept': "multipart/form-data",
        'Content-Type': "application/x-www-form-urlencoded; charset=utf-8",
        'Cookie': cookie,
        'User-Agent': "WeChatHelper/9.1.9 (iPhone; iOS 13.1.3; Scale/3.00)",
        'Accept-Language': "zh-Hans-CN;q=1",
        'Referer': "https://mp.weixin.qq.com/cgi-bin/masssend?action=get_appmsg_copyright_stat&token={}&lang=zh_CN".format(
            tooken),
        'cache-control': "no-cache",
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False)

    print(response.text)

    url = "https://mp.weixin.qq.com/cgi-bin/masssend"

    querystring = {'action': 'time_send', "t": "ajax-response", "token": tooken, "lang": "zh_CN"}
    payload = "token={}&lang=zh_CN&f=json&ajax=1&random=0.4981124445212717&smart_product=0&type=10&appmsgid={}&share_page=1&send_time={}&cardlimit=1sex=0&groupid=-1&synctxweibo=0&country=&province=&city=&imgcode=&operation_seq={}&req_id=GMpebl0ECNkRo1UQRn62HfEA7KaaFEmw&req_time={}&direct_send=1".format(
        tooken, app_id1, send_time, create_time1, time1)
    headers = {
        'Host': "mp.weixin.qq.com",
        'Accept': "multipart/form-data",
        'Content-Type': "application/x-www-form-urlencoded; charset=utf-8",
        'Cookie': cookie,
        'User-Agent': "WeChatHelper/9.1.9 (iPhone; iOS 13.1.3; Scale/3.00)",
        'Accept-Language': "zh-Hans-CN;q=1",
        'Referer': "https://mp.weixin.qq.com/cgi-bin/masssendpage?t=mass/send&token={}&lang=zh_CN".format(tooken),
        'cache-control': "no-cache"
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False).json()

    return response


user_list = csv.reader(open(path_user))
# print(user_list)
user_data_list = []
for user in user_list:
    # print(user)
    user_data_list.append(user)
user_list = user_data_list
for num in range(begin_user, end_user):
    # 调用浏览器登陆
    print(num)
    user = user_list[num]
    # 对得到得COOKIE,TOOKEN进行处理
    cookie_tooken = get_url(user)
    cookie = cookie_tooken[0]
    tooken = cookie_tooken[1]
    appid = get_appid(tooken, cookie)
    app_id = appid[0]
    create_time = appid[1]
    app_id1 = appid[2]
    # print(app_id1)
    create_time1 = appid[3]
    # print(create_time1)
    data_json = send_data(tooken, cookie, app_id, create_time)
    # print(data_json)
    if data_json['base_resp']['err_msg'] == 'ok':
        print('发布成功')
    else:
        if data_json['base_resp']['err_msg'] == 'ok':
            print('发布成功')
        else:
            data_json = send_data(tooken, cookie, app_id, create_time)
            print('正在发布')
            if data_json['base_resp']['err_msg'] == 'ok':
                print('发布成功')

            else:
                data_json = send_data(tooken, cookie, app_id, create_time)
                print('正在发布')
                if data_json['base_resp']['err_msg'] == 'ok':
                    print('发布成功')

                else:
                    print('{}账号自动发布失败'.format(user))
                    with open(r'C:\Users\Administrator\Desktop\发布失败的账号.csv', 'a', encoding='utf-8',
                              newline='') as f:
                        f_csv = csv.writer(f)
                        f_csv.writerow(user)
                        f.close()
    a = (int(time.time()))
    b = random.randrange(79200, 93600, 60)
    c = b + a
    d = c % 60
    send_time = str(c - d)
    send_json = send_time_data(tooken, cookie, app_id1, create_time1, send_time)
    if send_json['base_resp']['err_msg'] == 'ok':
        print('预设成功')
    else:
        if send_json['base_resp']['err_msg'] == 'ok':
            print('预设成功')
        else:
            send_json = send_time_data(tooken, cookie, app_id1, create_time1, send_time)
            print('正在预设')
            if send_json['base_resp']['err_msg'] == 'ok':
                print('预设成功')

            else:
                send_json = send_time_data(tooken, cookie, app_id1, create_time1, send_time)
                print('正在预设')
                if send_json['base_resp']['err_msg'] == 'ok':
                    print('预设成功')

                else:
                    print('{}账号自动预设失败'.format(user))
                    with open(r'C:\Users\Administrator\Desktop\预设失败的账号.csv', 'a', encoding='utf-8',
                              newline='') as f:
                        f_csv = csv.writer(f)
                        f_csv.writerow(user)
                        f.close()
