import requests
from bs4 import BeautifulSoup
import re

# 反爬虫策略
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31"
}
cookies ={
"Cookie": 'bid=UUJyGxdUAvE; __utmc=30149280; __utmz=30149280.1695283879.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ll="118183"; ap_v=0,6.0; viewed="1046265_1017143_1084336_10466265_2256039_1007305"; apiKey=; dbcl2="274656538:3TdXAga9IPc"; ck=k-Tx; frodotk_db="a537afb8776aee52efa70f296640caf6"; push_noty_num=0; push_doumail_num=0; __utma=30149280.1842746003.1695283879.1695551068.1695556724.6; __utmv=30149280.27465; __utmt_douban=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1695557428%2C%22https%3A%2F%2Fbook.douban.com%2F%22%5D; _pk_id.100001.8cb4=c54a4c010270bb6c.1695557428.; _pk_ses.100001.8cb4=1; __yadk_uid=UW01ZWrMf8VOdGNYSersEnPau2Hod9ry; __utmt=1; __utmb=30149280.26.9.1695557430361'
}

url = "https://movie.douban.com/subject/1292052/"
response = requests.get(url, headers=headers, cookies=cookies)
soup = BeautifulSoup(response.text, "html.parser")

# 查找指定区域的<a>标签

patten = r"\d+/"

recommendations_bd = soup.find("div", attrs={"class": "recommendations-bd"})
dd_tags = recommendations_bd.find_all("dd")

# 遍历每个<a>标签，获取其href属性
for dd_tag in dd_tags:
    a_tag = dd_tag.find("a")
    href = a_tag["href"]
    match = re.search(patten, href)
    if match:
        print(match.group()[:-1])
