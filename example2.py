import requests
from bs4 import BeautifulSoup
import re
import csv
import json
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46"
}
books = []
with open('Book_id.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        book_id = row[0]  # 获取书籍ID
        url = f'https://book.douban.com/subject/{book_id}'  # 构造书籍信息的URL
        response = requests.get(url, headers=headers)
        html = etree.HTML(response.text)
        content = html.xpath('//*[@id="link-report"]/span[@class="all hidden"]//p/text()')
        if len(content)==0:
            content = html.xpath('//*[@class="related_info"]/div[@id="link-report"]//p/text()')
        print(content)
