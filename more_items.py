import json
import random
import time
from ssl import SSLError

import bs4
import requests
from requests import RequestException

max_tries = 20
USER_AGENT_LIST = []
with open('D:\\UKWhisky\\User-Agent.txt') as f:
    lines = f.readlines()
    for line in lines:
        USER_AGENT_LIST.append(line.strip())

cookies = {
    'cookie_enabled': 'true',
    'ID': 'LTRSCBRDK8K00GW',
    'IDPWD': 'I44815973',
    'COOKIE_ID': 'N8VQC24WKXQ002D',
    'visit': 'N8VQC24WKXQ002D%7C20250308014424%7C%2F%7C%7Cend%20',
    'user_status': 'E%7C',
    'search': 'start%7Cjohnny%2Bwalker%2Bblue%2Bblend%2Bscotch%2Bwhisky%2Bscotland%7C1%7CUK%7CGBP%7C%7C%7C%7C%7C%7C%7C%7C%7Ce%7Ce%7C%7C%7CN%7C%7Ca%7C%7C%7C%7CCUR%7Cend',
    'adin': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NDMyMjk2NTAuOTQwNzE4LCJleHAiOjE3ODM0MDIwNTAuOTQwNzE4LCJ1aWQiOjQ4NTUxOCwidWVhIjoiZ2FveHVhbjA2MDZAMTYzLmNvbSIsInVhY2QiOiIyMDIzMTIxNSJ9.cIMTuMHebyuDqxJu6HJLX03BUlLpU1coLUT9SU29Cwg',
    '_csrf': 'eDtoNDqgUrNKygCdSvR3QqTSbDf8a1RK',
    'cookie_consent': 'allow',
    '_pxhd': 'wWEghYfrROeadmdY9Zf4DruU2Fr64ONoTEQ7anTZUvYDK31fqybYOwa3m/8mtSX8iJ/BrStyJpz3TIyskPROSw==:53s9VNMEVieLnb3uT85IVlESw/srrZZ6ZP2Ol4IFK4uVX5jxg9GNYu7ipTwGc6eSj60PT7fxd-EmIzfSK5f1uWrYo8qlmrmB3C6l-3wk0EA=',
    'pxcts': 'e08fc214-0c66-11f0-9f6f-7fc9f14e73b3',
    '_pxvid': 'dcda3f26-fbbe-11ef-a5c9-c2d0da3008fc',
    'find_tab': '',
    '_ga': 'GA1.1.1506201397.1741398266',
    '_px2': 'eyJ1IjoiZTcwNjQyNzAtMGM2Ni0xMWYwLWFiM2MtYmI4MjIwNzJhYTc1IiwidiI6ImRjZGEzZjI2LWZiYmUtMTFlZi1hNWM5LWMyZDBkYTMwMDhmYyIsInQiOjE3NDMyMzAxOTM4NjUsImgiOiIwODkxYjdlOGM0NWI1MGI2MThjM2Y5YTliYzQzM2IzMGQ5MThmYzI3YjI1M2FlYjJjNzliMTVjNDViNzVmNmY3In0=',
    '_px3': 'b0350a6a76ca13bee1e73f68ffb522915ee75830cd2217c4f541e5b2eaee498b:0Koar+0BadCaMJusqTmJxRM9VRMxy/X8R8e1j0R0wy7k9o+xKGobBLvVhyqdmlUAIoegzC6DM3EQ/3Fd1B8gIQ==:1000:nmbwvlCuGUdtrlbSHbcvFw35BABnfRrmHLhb2/G7gkgPc2ehdOmVYAk4jx7yldnDwLsEXllWEjP5abPT82RZq8CLzeXw9L7bRbp/eBfC0DoGFbMgrqAh88pcvJHYglhzFFS/oIylcDYj1lDrWaIM55k1chYtvM0KV1kIamu+J9wIFNYCZ5BBxBTIqaySqrRRy5SeAP1lqSHrRyYdUHuyUhfHI8TulpNvBE7uR9rmiPQ=',
    '_pxde': '2beb2b5841366434b8e301f318fac11e4fb599d491c6130f773e798543fcb455:eyJ0aW1lc3RhbXAiOjE3NDMyMjk4OTM4NjUsImZfa2IiOjAsImlwY19pZCI6W119',
    'NPS_bc24fa74_last_seen': '1741398270974',
    '_ga_M0W3BEYMXL': 'GS1.1.1743229648.7.1.1743229678.0.0.0',
}

headers = {
    'authority': 'www.wine-searcher.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': random.choice(USER_AGENT_LIST)  # 使用随机User-Agent
}

# 快代理相关参数（根据用户提供的示例填写）
KUAI_SECRET_ID = "of27pvy1mnp2st493scp"
KUAI_SIGNATURE = "s58m81icas4xpo94xzl29gxi2nxp2769"
KUAI_USERNAME = "d4417206438"
KUAI_PASSWORD = "AAAaaa111"
KUAI_API_URL = "https://dps.kdlapi.com/api/getdps/"

def get_proxies():
    """获取快代理的代理IP"""
    params = {
        "secret_id": KUAI_SECRET_ID,
        "signature": KUAI_SIGNATURE,
        "num": 1,
        "pt": 1,  # 高匿代理
        "sep": 1  # 返回格式为IP:PORT
    }
    try:
        response = requests.get(KUAI_API_URL, params=params, timeout=5)
        response.raise_for_status()
        proxy_ip = response.text.strip()
        proxy_url = f"http://{KUAI_USERNAME}:{KUAI_PASSWORD}@{proxy_ip}"
        return {
            "http": proxy_url,
            "https": proxy_url
        }
    except Exception as e:
        print(f"获取代理失败: {str(e)}")
        return None

def get_more_items(year, p):
    params = {
        'p': p,
        '_pjax': '#pjax-offers',
    }
    for i in range(max_tries):
        try:
            # 使用随机User-Agent
            current_user_agent = random.choice(USER_AGENT_LIST)
            headers['user-agent'] = current_user_agent
            proxies = get_proxies()
            if proxies is None:
                print("无法获取有效代理，跳过此次请求")
                continue
            
            response = requests.get(
                f'https://www.wine-searcher.com/find/whiskey/{year}/uk/-/a/1',
                params=params,
                headers=headers,
                proxies=proxies,
                cookies=cookies,
                timeout=10  # 设置请求超时时间
            )
            response.raise_for_status()
            new_cookies = response.cookies.get_dict()
            if new_cookies:
                cookies.update(new_cookies)
            return response.text
        except (RequestException, SSLError) as req_error:
            print(f"请求出错: {str(req_error)}，重试第 {i+1}/{max_tries} 次...")
            time.sleep(random.uniform(2, 4))
    
    print(f"超过最大重试次数，无法获取 {year} 年第 {p} 页数据")
    return None

def parse_more_items(html):
    if html is None:
        return None
    soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        all_whiskey = soup.find_all('div', class_='col-12 col-sm-6 col-md-6 col-lg-4')
    except AttributeError:
        return None
    if not all_whiskey:
        return None
    return [f'https://www.wine-searcher.com{a["href"]}' 
            for a in soup.select('div.col-12 a')]

def return_whiskey_url(year, p):
    html = get_more_items(year, p)
    return parse_more_items(html)

if __name__ == "__main__":
    # 测试代理是否正常
    test_url = "https://dev.kdlapi.com/testproxy"
    proxies = get_proxies()
    if proxies:
        try:
            response = requests.get(test_url, proxies=proxies, timeout=5)
            print("代理测试结果:", response.text)
        except Exception as e:
            print("测试失败:", str(e))
    else:
        print("未获取到可用代理")

