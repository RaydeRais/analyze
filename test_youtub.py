import requests
from more_items import get_proxies
cookies = {
    'GPS': '1',
    'YSC': 'im00MtHm5Oo',
    'VISITOR_INFO1_LIVE': 'rrfiW_efTXA',
    'VISITOR_PRIVACY_METADATA': 'CgJISxIEGgAgWg%3D%3D',
    'PREF': 'f4=4000000&f6=40000000&tz=Asia.Shanghai',
    'CONSISTENCY': 'AKreu9s-DalLTH03zgPW7JFawezsA0aklSmWS-IepXyuYKKSe3nW_nf398eHRqj7uCDtjzh_tldrWmGu4pfwzl_NV8V2KECIRGFQ9dgLdcLBpy2e_GInSHUutSNuuaAPTdLblmvxNcYu4fMgsSMmsh8',
}

headers = {
    'authority': 'www.youtube.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    # 'cookie': 'GPS=1; YSC=im00MtHm5Oo; VISITOR_INFO1_LIVE=rrfiW_efTXA; VISITOR_PRIVACY_METADATA=CgJISxIEGgAgWg%3D%3D; PREF=f4=4000000&f6=40000000&tz=Asia.Shanghai; CONSISTENCY=AKreu9s-DalLTH03zgPW7JFawezsA0aklSmWS-IepXyuYKKSe3nW_nf398eHRqj7uCDtjzh_tldrWmGu4pfwzl_NV8V2KECIRGFQ9dgLdcLBpy2e_GInSHUutSNuuaAPTdLblmvxNcYu4fMgsSMmsh8',
    'referer': 'https://www.youtube.com/index',
    'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version-list': '"Not A(Brand";v="99.0.0.0", "Microsoft Edge";v="121.0.2277.4", "Chromium";v="121.0.6167.16"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"15.0.0"',
    'sec-ch-ua-wow64': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'service-worker-navigation-preload': 'true',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
}

response = requests.get('https://www.youtube.com/', headers=headers,proxies=get_proxies())
print(response.status_code)
print(response.text)