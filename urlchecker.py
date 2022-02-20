"""
url alive checker By ven0m

使用方法:
python3 urlchecker.py url.txt
"""

from typing import Tuple
from prettytable import PrettyTable
import requests
from lxml.html import fromstring
import sys

x = PrettyTable()
x.field_names = ['num', 'URL', 'status_code', 'title', 'result']
x.align['title'] = 'l'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

"""
拼接url
分别返回http和https两种url
"""
def splicing_url(input_str: str) -> Tuple:
    """
    拼接url
    :param input_str:
    :return: 元组。 len:2, [0]:http字符串， [1]: https字符串
    """
    if input_str.startswith('http://'):
        result_http, result_https = input_str, 'https' + input_str[4:]
    elif input_str.startswith('https://'):
        result_http, result_https = 'http' + input_str[5:], input_str
    else:
        result_http, result_https = 'http://' + input_str, 'https://' + input_str
    if input_str[-1] != '/':
        result_http += '/'
        result_https += '/'
    return result_http, result_https

"""
判断返回respnose code
"""
def requestor(httpurl: str,httpsurl: str) -> Tuple:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    try:
        req1 = requests.get(httpurl,timeout=5,headers=headers)
        code1 = req1.status_code
    except:
        #超时code置0
        code1 = 0
        pass
    try:
        req2 = requests.get(https_url,timeout=5,headers=headers)
        code2 = req2.status_code
    except:
        # 超时code置0
        code2 = 0
        pass
    return code1,code2


try:
    urlfile = sys.argv[1]
except:
    print("Please input url file")
    exit(0)

with open('url1.txt', 'rt', newline='') as u:
    urls = u.read().splitlines()
    i = 0
    for url in urls:
        try:
            http_url, https_url = splicing_url(url)
            http_code, https_code = requestor(http_url, https_url)
            if http_code == 0 and https_code==0:
                print("[-]" + '\t' + url + ": Not Alive")

            elif http_code != 0 and https_code==0:
                http_req = requests.get(http_url, headers=headers)
                http_status_code = http_req.status_code
                try:
                    tree = fromstring(http_req.content)
                    http_title = tree.findtext('.//title')
                except:
                    http_title = "null"
                    pass
                i = i + 1
                x.add_row([i, http_url, http_status_code, http_title, 'Vulnerability'])
                print("[+]" + '\t' + http_url + '\t' + str(http_status_code) + '\t' + str(http_title))

            elif http_code == 0 and https_code != 0:
                https_req = requests.get(https_url, headers=headers)
                try:
                    tree = fromstring(https_req.content)
                    https_title = tree.findtext('.//title')
                except:
                    https_title = "null"
                    pass
                https_status_code = https_req.status_code
                i = i + 1
                x.add_row([i, https_url, https_status_code, https_title, 'Vulnerability'])
                print("[+]" + '\t' + https_url + '\t' + str(https_status_code) + '\t' + https_title)

            elif http_code == 200 and https_code == 200:
                http_req = requests.get(http_url, headers=headers)
                https_req = requests.get(https_url, headers=headers)
                http_status_code = http_req.status_code
                https_status_code = https_req.status_code
                try:
                    http_tree = fromstring(http_req.content)
                    http_title = http_tree.findtext('.//title')
                except:
                    http_title = "null"
                    pass
                try:
                    https_tree = fromstring(https_req.content)
                    https_title = https_tree.findtext('.//title')
                except:
                    https_title = "null"
                    pass
                i = i + 1
                print("[+]" + '\t' + http_url + '\t' + str(http_status_code) + '\t' + http_title)
                print("[+]" + '\t' + https_url + '\t' + str(https_status_code) + '\t' + https_title)
                x.add_row([i, http_url, http_status_code, http_title, 'Vulnerability'])
                x.add_row([i, https_url, https_status_code, https_title, 'Vulnerability'])
        except Exception as e:
            pass
        continue

print(x)
with open('result.txt', 'w') as result_file:
    result_file.write(str(x))
    result_file.close()