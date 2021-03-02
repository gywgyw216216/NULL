#!usr/bin/env python
# -*- coding: utf-8 -*-

from math import ceil
from time import strftime, sleep
from datetime import datetime, timedelta
from random import uniform
from requests import Session
from bs4 import BeautifulSoup
from sys import argv



RSA_E = "010001"
RSA_M = \
    "008aed7e057fe8f14c73550b0e6467b023616ddc8fa91846d2613cdb7f7621e3cada4cd5d812d627af6b87727ade4e26d26208b7326815941492b2204c3167ab2d53df1e3a2c9153bdb7c8c2e968df97a5e7e01cc410f92c4c2c2fba529b3ee988ebc1fca99ff5119e036d732c368acf8beba01aa2fdafa45b21e4de4928d0d403"



def print_log(string):
    print(strftime("%Y-%m-%d %H:%M:%S") + "\t" + string)



def get_rsa_password(password, e, m):
    # Reference: https://www.cnblogs.com/himax/p/python_rsa_no_padding.html
    m = int.from_bytes(bytearray.fromhex(m), byteorder='big')
    e = int.from_bytes(bytearray.fromhex(e), byteorder='big')
    plain_text = password[::-1].encode("utf-8")
    input_nr = int.from_bytes(plain_text, byteorder='big')
    crypted_nr = pow(input_nr, e, m)
    key_length = ceil(m.bit_length() / 8)
    crypted_data = crypted_nr.to_bytes(key_length, byteorder='big')
    
    return crypted_data.hex()



def login_by_webvpn(username, password):
    session = Session()
    session.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,"
                  "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
        "origin": "https://webvpn.sues.edu.cn"
    })
    result1 = session.get("https://webvpn.sues.edu.cn/")
    soup1 = BeautifulSoup(result1.content, "lxml")
    cas_url = soup1.find("a")["href"]
    result2 = session.get(cas_url)
    soup2 = BeautifulSoup(result2.content, "lxml")
    execution = soup2.find("input", {"name": "execution"}).attrs["value"]
    data = {
        "username": username, "password": get_rsa_password(password, RSA_E, RSA_M), "execution": execution,
        "encrypted": "true", "_eventId": "submit", "loginType": "1", "submit": "登 录"
    }
    post_target = soup2.find("form")["action"]
    result3 = session.post(post_target, data)
    soup3 = BeautifulSoup(result3.content, "lxml")
    
    if "健康信息填报" not in soup3.text:
        return False, "Fail to Login! ", None, None
    
    target_url = "https://webvpn.sues.edu.cn" + soup3.find("a", {"title": "健康信息填报"})["href"]
    session.get(target_url)
    sleep(5)
    result4 = session.get(target_url)
    
    return True, "Login Successfully! ", result4.url, session



def report_by_webvpn(username, password):
    state, message, report_url, session = login_by_webvpn(username, password)
    
    if not state:
        return False, message
    
    session.get(report_url)
    url_header = "/".join(report_url.split("/")[:-1])
    
    time_utc = datetime.utcnow()
    Beijing_time = (time_utc + timedelta(hours=8))
    
    if Beijing_time.hour % 24 < 12:
        period = "上午"
    else:
        period = "下午"
    
    now = Beijing_time.strftime("%Y-%m-%d %H:%M")
    print_log("Beijing Time: " + now + "\t" + period)
    second_request_json = {
        "params": {"empcode": username}, "querySqlId": "com.sudytech.work.shgcd.jkxxcj.jkxxcj.queryNear"
    }
    session.headers.update({"referer": report_url})
    second_result = session.post(url_header + "/com.sudytech.portalone.base.db.queryBySqlWithoutPagecond.biz.ext",
                                 json=second_request_json)
    second_result.url, second_result.content.decode()
    
    if len(second_result.json()["list"]) == 0:
        return False, "Fail to Get Last Report! "
    
    person = second_result.json()["list"][0]
    update_data = {
        "params": {
            "sqrid": person["SQRID"], "sqbmid": person["SQBMID"], "rysf": person["RYSF"], "sqrmc": person["SQRMC"],
            "gh": person["GH"], "sfzh": person["SFZH"], "sqbmmc": person["SQBMMC"], "xb": person["XB"],
            "lxdh": person["LXDH"], "nl": person["NL"], "tjsj": now, "xrywz": person["XRYWZ"], "sheng": person["SHENG"],
            "shi": person["SHI"], "qu": person["QU"], "jtdzinput": person["JTDZINPUT"], "gj": person["GJ"],
            "jtgj": person["JTGJ"], "jkzk": person["JKZK"], "jkqk": person["JKQK"],
            "tw": str(round(uniform(36.5, 36.8), 1)), "sd": period, "bz": person["BZ"], "_ext": "{}"
        }
    }
    print_log(update_data["params"]["gh"] + "\t" + update_data["params"]["tw"] + "°C")
    url = url_header + "/com.sudytech.work.shgcd.jkxxcj.jkxxcj.saveOrUpdate.biz.ext"
    final_result = session.post(url, json=update_data)
    
    if final_result.json()['result']["success"]:
        return True, None
    else:
        return False, "[" + final_result.json()['result']['errorcode'] + "]" + final_result.json()['result']['msg']



if __name__ == '__main__':
    person = {"CASUsername": argv[1], "CASPassword": argv[2]}
    state1, message1, url, session = login_by_webvpn(person["CASUsername"], person["CASPassword"])
    
    if state1:
        print_log("Login SUES CAS Successfully! ")
    else:
        print_log("Fail to Login SUES CAS! ")
        quit()
    
    state2, message2 = report_by_webvpn(person["CASUsername"], person["CASPassword"])
    
    if state2:
        print_log("Report Successfully! ")
    else:
        print_log("Fail to Report! \t" + message2)
