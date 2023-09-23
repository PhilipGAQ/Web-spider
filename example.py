import requests
from bs4 import BeautifulSoup
import re

# 反爬策略
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46"
}
url = "https://movie.douban.com/top250"

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

role_intro_section = soup.find("ol", class_="grid_view")
# Find all role entries
role_entries = role_intro_section.find_all("li")
# Loop through each role entry and extract the relevant information
# actor = role_entry.dd.a.get_text()
# description = role_entry.dd.get_text()
# Image is in a different tag
# image = role_entry.find('img')['src']

# Append role information to list
# roles.append([name, actor, description, image])
# 补全代码将所有的name写入文件
with open("names.txt", "w") as file:
    for role_entry in role_entries:
        # "info".*?正则表达式
        name = re.findall(
            'div.*?"info".*?"hd".*?span.*?"title">(.*?)</span>', str(role_entry), re.S
        )

        file.write(name[0] + "\n")
