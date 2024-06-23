import requests
from bs4 import BeautifulSoup
import re

# 定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://cf.090227.xyz/',
    'Referer': 'https://stock.hostmonit.com/',
    'Referer': 'https://ip.164746.xyz/',
    'Referer': 'https://monitor.gacjie.cn/',
    'Referer': 'https://345673.xyz/'
}

# 定义五个网址
urls = [
    "https://cf.090227.xyz/",
    "https://stock.hostmonit.com/CloudFlareYes",
    "https://ip.164746.xyz/",
    "https://monitor.gacjie.cn/page/cloudflare/ipv4.html",
    "https://345673.xyz"
]

# 处理每个网址的数据
def process_site_data(url):
    soup = extract_table_data(url)
    if not soup:
        return []

    data = []
    if "cf.090227.xyz" in url:
        rows = soup.find_all('tr')
        for row in rows:
            line_name_elem = row.find('th', string=re.compile(r'线路'))
            if line_name_elem:
                line_name = line_name_elem.find_next('td').text.strip()
            else:
                continue
            
            ip_address_elem = row.find('th', string=re.compile(r'IP'))
            if ip_address_elem:
                ip_address = ip_address_elem.find_next('td').text.strip()
            else:
                continue
            
            latency_elem = row.find('th', string=re.compile(r'平均延迟'))
            if latency_elem:
                latency_text = latency_elem.find_next('td').text.strip()
                latency_match = latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    latency_unit = 'ms'
                    data.append(f"{ip_address}#{line_name}-{latency_value}{latency_unit}")

    elif "stock.hostmonit.com" in url:
        rows = soup.find_all('tr', class_=re.compile(r'el-table__row'))
        for row in rows:
            line_name_elem = row.find('td', class_=re.compile(r'column_1?'))
            if line_name_elem:
                line_name = line_name_elem.text.strip()
            else:
                continue
            
            ip_address_elem = row.find('td', class_=re.compile(r'column_2?'))
            if ip_address_elem:
                ip_address = ip_address_elem.text.strip()
            else:
                continue
            
            latency_elem = row.find('td', class_=re.compile(r'column_3?'))
            if latency_elem:
                latency_text = latency_elem.text.strip()
                latency_match = latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    latency_unit = 'ms'
                    data.append(f"{ip_address}#{line_name}-{latency_value}{latency_unit}")

    elif "ip.164746.xyz" in url:
        rows = soup.find_all('tr')
        for row in rows:
            ip_address_elem = row.find('td', string=re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'))
            if ip_address_elem:
                ip_address = ip_address_elem.text.strip()
            else:
                continue
            
            latency_elem = row.find_all('td')[4]  # 第五列是延迟数据
            if latency_elem:
                latency_text = latency_elem.text.strip()
                latency_match = latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    latency_unit = 'ms'
                    data.append(f"{ip_address}-{latency_value}{latency_unit}")
    
    elif "monitor.gacjie.cn" in url:
        rows = soup.find_all('tr')
        for row in rows:
            line_name_elem = row.find('td', string=re.compile(r'线路名称'))
            if line_name_elem:
                line_name = line_name_elem.find_next('td').text.strip()
            else:
                continue
            
            ip_address_elem = row.find('td', string=re.compile(r'优选地址'))
            if ip_address_elem:
                ip_address = ip_address_elem.find_next('td').text.strip()
            else:
                continue
            
            latency_elem = row.find('td', string=re.compile(r'往返延迟'))
            if latency_elem:
                latency_text = latency_elem.find_next('td').text.strip()
                latency_match = latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    latency_unit = 'ms'
                    data.append(f"{ip_address}#{line_name}-{latency_value}{latency_unit}")
    
    elif "345673.xyz" in url:
        rows = soup.find_all('tr')
        for row in rows:
            line_name_elem = row.find('td', string=re.compile(r'线路名称'))
            if line_name_elem:
                line_name = line_name_elem.find_next('td').text.strip()
            else:
                continue
            
            ip_address_elem = row.find('td', string=re.compile(r'优选地址'))
            if ip_address_elem:
                ip_address = ip_address_elem.find_next('td').text.strip()
            else:
                continue
            
            latency_elem = row.find('td', string=re.compile(r'平均延迟'))
            if latency_elem:
                latency_text = latency_elem.find_next('td').text.strip()
                latency_match = latency_pattern.match(latency_text)
                if latency_match:
                    latency_value = latency_match.group(1)
                    latency_unit = 'ms'
                    data.append(f"{ip_address}#{line_name}-{latency_value}{latency_unit}")

    return data

# 主函数，处理所有网站的数据
def main():
    all_data = []
    for url in urls:
        site_data = process_site_data(url)
        all_data.extend(site_data)
    
    # 去除重复的IP地址行
    unique_data = list(set(all_data))

    # 过滤延迟数据低于100ms的行
    filtered_data = [line for line in unique_data if float(line.split('-')[-1].replace('ms', '')) < 100]

    # 写入到ips_latency.txt文件
    with open('ips_latency.txt', 'w', encoding='utf-8') as f:
        for line in filtered_data:
            f.write(line + '\n')

if __name__ == "__main__":
    main()
