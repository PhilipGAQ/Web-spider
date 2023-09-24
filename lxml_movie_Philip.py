import requests
from bs4 import BeautifulSoup
import re
import csv
import json
from lxml import etree

# 为电影创建一个json字典
movie = {
    "title": "The Shawshank Redemption",
    "year": 1994,
    "starring": ["Tim Robbins", "Morgan Freeman"],
    "director": "Frank Darabont",
    "genre": ["Drama", "Crime"],
    "rating": 9.3,
    "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    "cast": ["Tim Robbins", "Morgan Freeman"],
    "duration": 142,  # 电影时长（分钟）
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46"
}
Movies = []
with open("Movie_id.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        movie_id = row[0]  # 获取书籍ID
        url = f"https://book.douban.com/subject/{movie_id}"  # 构造书籍信息的URL
        response = requests.get(url, headers=headers)
        html = etree.HTML(response.text)
        # 读取title year director genre rating plot cast duration comments
        # title
        title = html.xpath("/html/body/div[3]/div[1]/h1/span[1]/text()")
        # year
        year = html.xpath("/html/body/div[3]/div[1]/h1/span[2]/text()")
        # director
        director = html.xpath(
            "/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]/span[2]/a/text()"
        )
        # genre
        genre = html.xpath("/html/body/div[3]/div[1]/div[1]/div[1]/span[2]/text()")
        # rating
        rating = html.xpath(
            "/html/body/div[3]/div[1]/div[2]/div/div[1]/div[1]/strong/text()"
        )
        # starring TODO

        # plot

        plot = html.xpath(
            "/html/body/div[3]/div[2]/div/div[1]/div[3]/div[1]/span[2]/div/div/p/text()"
        )
        if len(plot) == 0:
            plot = html.xpath(
                '//*[@class="related_info"]/div[@id="link-report"]//p/text()'
            )
        # print(plot) now save it
