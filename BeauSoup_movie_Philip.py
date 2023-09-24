import requests
from bs4 import BeautifulSoup
import re
import csv
import json

# 为电影创建一个json字典
movie = {
    "title": "The Shawshank Redemption",
    "year": 1994,
    "director": "Frank Darabont",
    "genre": ["Drama", "Crime"],
    "rating": 9.3,
    "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    "cast": ["Tim Robbins", "Morgan Freeman"],
    "duration": 142,  # 电影时长（分钟）
}

# 反爬虫策略
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46"
}


# open the file to read and to save
with open("Movie_id.csv", mode="r") as movielist:
    # read the file
    csv_reader = csv.reader(movielist)
    for row in csv_reader:
        # get the full url
        url_head = "https://movie.douban.com/subject/"
        url_tail = str(row)
        url = url_head + url_tail[2:-2]
        # print(url)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        span_element = soup.find("span", class_="all hidden")
        if span_element is not None:
            print(span_element.text)
            # 将爬到的数据存入字典
            movie["plot"] = span_element.text

            # 使用.text属性获取<span>元素中的文本内容
        else:
            # print("Couldn't find intro, whose url=", url_tail)
            span_element = soup.find("span", attrs={"property": "v:summary"})
            if span_element is not None:
                print(span_element.text)
            else:
                print("Couldn't find intro, whose url=", url_tail)
