# config.py 自定义配置,包括阅读次数、推送token的填写
import os
import re

"""
可修改区域
默认使用本地值如果不存在从环境变量中获取值
"""


# 阅读次数(每次30秒)
READ_NUM = 2*60
# 需要推送时可选，可选pushplus、wxpusher、telegram
PUSH_METHOD = "" or os.getenv('PUSH_METHOD')
# pushplus推送时需填
PUSHPLUS_TOKEN = "" or os.getenv("PUSHPLUS_TOKEN")
# telegram推送时需填
TELEGRAM_BOT_TOKEN = "" or os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "" or os.getenv("TELEGRAM_CHAT_ID")
# wxpusher推送时需填
WXPUSHER_SPT = "" or os.getenv("WXPUSHER_SPT")
# read接口的bash命令，本地部署时可对应替换headers、cookies
curl_str = os.getenv('WXREAD_CURL_BASH')

# headers、cookies是一个省略模版，本地或者docker部署时对应替换
cookies = {}
headers = {}


"""
建议保留区域|默认读三体，其它书籍自行测试时间是否增加
"""
data ={
  "appId": "wb182564874663h152492176",
  "b": "ce032b305a9bc1ce0b0dd2a",
  "c": "7cb321502467cbbc409e62d",
  "ci": 70,
  "co": 0,
  "sm": "[插图]第三部广播纪元7年，程心艾AA说",
  "pr": 74,
  "rt": 30,
  "ts": 1727660516749,
  "rn": 31,
  "sg": "991118cc229871a5442993ecb08b5d2844d7f001dbad9a9bc7b2ecf73dc8db7e",
  "ct": 1727660516,
  "ps": "b1d32a307a4c3259g016b67",
  "pc": "080327b07a4c3259g018787",
  "s": "44f82a10"
}

# 章节内位置，对应参数co
cos = [389,609,745,803,981,1154]

# 章节目录，每个数组内参数依次为ci、c、pr
# 这里的书籍是三体，参数b="ce032b305a9bc1ce0b0dd2a"
chapters = [
    [9,  "f4b32ef025ef4b9ec30acd6", 1],
    [10, "81232fb025f812b4ba28a23", 1],
    [11, "2663284026026657d5ffeed", 1],
    [12, "e2e329c0261e2ef524fbf75", 1],
    [13, "ed332ca0262ed3d2c2191f2", 1],
    [14, "ac6325b0263ac627ab1c3dd", 3],
    [15, "f8932dd0264f899139df0ae", 4],
    [16, "38b3252026538b3eff8b041", 4],
    [17, "ec8325e0266ec89566376b5", 4],
    [18, "697324802676974ce5aceab", 4],
    [19, "c9e32940268c9e1074f5bc6", 7],
    [20, "65b326f026965b9eea6e6e1", 7],
    [21, "f09320f026af0935e4cd23d", 7],
    [22, "a973204026ba97da629bd12", 7],
    [23, "a3c320b026ca3c65c297000", 9],
    [24, "272329d026d2723d092b535", 9],
    [25, "5f9323e026e5f93f9835418", 9],
    [26, "6983268026f698d51a198ff", 11],
    [27, "7f632b502707f6ffaa6bf2e", 11],
    [28, "7323297027173278a4a8f1d", 11],
    [29, "5fd32dd02725fd0b37cd75e", 11],
    [30, "2b4324802732b44928aee17", 11],
    [31, "c45328f0274c45147dee704", 11],
    [32, "eb132680275eb160de1d35c", 11],
    [33, "5ef32bd02765ef0599381f7", 11],
    [34, "07e323f027707e1cd7dc674", 11],
    [35, "da432420278da4fb5c6e9ad", 15],
    [36, "4c5327a02794c56ff4ce24c", 15],
    [37, "a0a32dd027aa0a080f42962", 15],
    [38, "2023270027b202cb962a56f", 15],
    [39, "c8f3245027cc8ffe9a588b8", 15],
    [40, "3de32dd027d3def184ad06e", 15],
    [41, "06932ec027e069059b7e512", 15],
    [42, "ec532f2027fec5decca5182", 15],
    [43, "76d325c028076dc611d6d8c", 15],
    [44, "d1f32250281d1f491a40045", 15],
    [45, "9b832a602829b86192511b5", 15]
]


def convert(curl_command):
    """提取bash接口中的headers与cookies
    支持 -H 'Cookie: xxx' 和 -b 'xxx' 两种方式的cookie提取
    """
    # 提取 headers
    headers_temp = {}
    for match in re.findall(r"-H '([^:]+): ([^']+)'", curl_command):
        headers_temp[match[0]] = match[1]

    # 提取 cookies
    cookies = {}
    
    # 从 -H 'Cookie: xxx' 提取
    cookie_header = next((v for k, v in headers_temp.items() 
                         if k.lower() == 'cookie'), '')
    
    # 从 -b 'xxx' 提取
    cookie_b = re.search(r"-b '([^']+)'", curl_command)
    cookie_string = cookie_b.group(1) if cookie_b else cookie_header
    
    # 解析 cookie 字符串
    if cookie_string:
        for cookie in cookie_string.split('; '):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
    
    # 移除 headers 中的 Cookie/cookie
    headers = {k: v for k, v in headers_temp.items() 
              if k.lower() != 'cookie'}

    return headers, cookies


headers, cookies = convert(curl_str) if curl_str else (headers, cookies)
