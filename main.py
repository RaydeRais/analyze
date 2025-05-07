import json
import os
import random
import re
import time
from ssl import SSLError

import bs4
import pandas as pd
import requests
from requests import RequestException

# 从 more_items.py 导入需要的变量和函数
from more_items import return_whiskey_url, get_proxies, cookies, headers, max_tries

def get_list_html(url):
    for i in range(1, max_tries):
        try:
            response = requests.get(url, headers=headers, proxies=get_proxies(), cookies=cookies)
            response.raise_for_status()
            new_cookies = response.cookies.get_dict()
            if new_cookies:
                cookies.update(new_cookies)
            return response.text
        except (RequestException, SSLError) as req_error:
            print(f'Exception occurred: {req_error}')
            print(f'Retrying ({i}/{max_tries})...')
            time.sleep(random.randint(2, 4))
    print(f'Max retries exceeded. Unable to fetch {url}.')
    return None

def parse_html_get_whiskey_url(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    product_num = soup.find('div', class_='font-weight-bold pl-1').text.strip().split(' ')[0]
    all_whiskey = soup.find_all('div', class_='col-12 col-sm-6 col-md-6 col-lg-4')
    if all_whiskey is None:
        return None
    all_whiskey_url2 = []
    for whiskey in all_whiskey:
        href = whiskey.find('a')['href']
        all_whiskey_url2.append(f'https://www.wine-searcher.com{href}')
    return product_num, all_whiskey_url2

def get_whiskey_html(whiskey_url):
    for i in range(1, max_tries):
        try:
            response = requests.get(whiskey_url.split('?')[0] + '?Xcurrencycode=GBP&Xsavecurrency=Y', 
                                   headers=headers, proxies=get_proxies(), cookies=cookies)
            response.raise_for_status()
            new_cookies = response.cookies.get_dict()
            if new_cookies:
                cookies.update(new_cookies)
            return response.text
        except (RequestException, SSLError) as req_error:
            print(f'Exception occurred: {req_error}')
            print(f'Retrying ({i}/{max_tries})...')
            time.sleep(random.randint(2, 4))
    print(f'Max retries exceeded. Unable to fetch {whiskey_url}.')
    return None

def parse_html_get_whiskey_info(html, in_name):
    html_string = html

    # 提取 name（正则表达式）
    name_match = re.search(
        r'<h1\s+class=["\']h2\s+mb-0["\'][^>]*>\s*(.*?)\s*</h1>',
        html_string,
        re.IGNORECASE | re.DOTALL
    )
    name = name_match.group(1).strip() if name_match else in_name.replace('+', ' ')
    
    html_string = html
    origin_match = re.search(r'From\s*<span[^>]*>([^<]+)<', html_string)
    origin = origin_match.group(1).strip() if origin_match else "Not found"

    price_match = re.search(r'Avg. Price.*?<b class="font-light-bold">(.*?)</b>', html_string, re.S)
    price = price_match.group(1).strip() if price_match else "Not found"

    grape_match = re.search(r'class="font-light-bold text-primary info-card__item-link-text text-underline">([^<]+)<', html_string)
    grape = grape_match.group(1).strip() if grape_match else "Not found"

    # 提取 currency（关键代码）
    # 提取 currency 和 price（兼容新旧结构）
    # 新结构：class="price text-nowrap"
    price_currency_match = re.search(
        r'<span\s+class=["\']price\s+text-nowrap["\'][^>]*>\s*(.*?)\s*<span\s+class=["\']font-light-bold["\']>(.*?)</span>',
        html_string,
        re.IGNORECASE | re.DOTALL
    )
    if price_currency_match:
        currency_part = price_currency_match.group(1).strip()
        # 提取符号（如 £, €, $）
        currency = re.search(r'[£€$]', currency_part)
        currency = currency.group() if currency else "Not found"
        price = price_currency_match.group(2).strip()
    else:
        # 回退到旧结构：class="small" 和 Avg. Price
        currency_old_match = re.search(
            r'<span\s+class=["\']small["\']>\s*([£€$])\s*</span>',
            html_string,
            re.IGNORECASE
        )
        currency = currency_old_match.group(1).strip() if currency_old_match else "Not found"


    

    return [{
        'name': name,
        'origin': origin.replace(' ', '').strip(),
        'price': price,
        'currency': currency, # 新增字段
        'grape': grape,
        'specs': '750ml'
    }]

def save_data_to_excel(data_list, excel_filename='whiskey_info.xlsx'):
    whiskey_df = pd.DataFrame(data_list)
    try:
        existing_data = pd.read_excel(excel_filename)
        combined_data = pd.concat([existing_data, whiskey_df], ignore_index=True)
        combined_data.to_excel(excel_filename, index=False)
    except FileNotFoundError:
        whiskey_df.to_excel(excel_filename, index=False)

def check_and_get_offset(year):
    file_name = f'whiskey_info{year}.xlsx'
    if os.path.exists(file_name):
        df = pd.read_excel(file_name)
        num_visited_urls = len(df)
        print(f'Found {num_visited_urls} visited URLs for year {year}.')
        return num_visited_urls
    else:
        print(f'File {file_name} not found. Starting from the beginning.')
        return 0

if __name__ == '__main__':
    years = ['1974']  # 可根据需要修改年份列表
    for year in years:
        print(f'curr year is {year}')
        if os.path.exists(f'./urls/{year}_url.txt'):
            print(f'有缓存{year}')
            with open(f'./urls/{year}_url.txt', 'r') as f:
                all_whiskey_url = [line.strip() for line in f.readlines()]
        else:
            print(f'没有缓存{year}')
            base_url = f'https://www.wine-searcher.com/find/whiskey/{year}/uk'
            page_html = None
            while page_html is None:
                page_html = get_list_html(base_url)
            product_num2, all_whiskey_url = parse_html_get_whiskey_url(page_html)
            product_num = '6700'  # 替换为实际产品数量
            
            if int(product_num) > 50:
                for p in range(1, 21):
                    print(f'当前数量大于50，这是第{p}页')
                    more_urls = return_whiskey_url(year, p * 50 + 1)
                    while more_urls is None or more_urls == []:
                        more_urls = return_whiskey_url(year, p * 50 + 1)
                    all_whiskey_url.extend(more_urls)
            
            with open(f'./urls/{year}_url.txt', 'w') as f:
                f.write('\n'.join(all_whiskey_url))
        
        print(f'当前{year} 的 whiskey 数量为 {len(all_whiskey_url)}')
        offset = check_and_get_offset(year)
        print(f'当前{year} 的 offset 为 {offset}')
        
        for idx, whiskey_url in enumerate(all_whiskey_url[offset:], start=offset):
            time.sleep(2)
            print(f'Current idx is {idx} Current whiskey_url is {whiskey_url}')
            w_html = None
            while w_html is None:
                w_html = get_whiskey_html(whiskey_url)
            data = parse_html_get_whiskey_info(w_html, in_name=whiskey_url.split('/find/')[-1].split('/2000/')[0])
            save_data_to_excel(data, f'data/whiskey_info{year}.xlsx')
            print(f'Saved {data} to Excel.')