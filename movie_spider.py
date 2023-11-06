import requests
from bs4 import BeautifulSoup
import re
import csv
import json
import time

# 为电影创建一个json字典
movie = {
    "num": "1",  # 电影编号，从1开始
    "id": "1292052",
    "title": "The Shawshank Redemption",
    "year": 1994,
    "director": "Frank Darabont",
    "genre": ["Drama", "Crime"],
    "country": ["USA"],
    "language": ["English"],
    "release date":"1994-09-10",
    "aka":"月黑高飞(港)",
    "IMDb":"tt0111161",
    "rating": 9.3,
    "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    "cast": ["Tim Robbins", "Morgan Freeman"],
    "duration": 142,  # 电影时长（分钟）
    "id_recommendations": ["114514"]
}

# 反爬虫策略
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31"
}
cookies ={
    "Cookie": 'll="118183"; bid=ozDG5P03_RM; __utmc=30149280; frodotk_db="49e7f3024834c33bddb7d906d89e49b1"; push_noty_num=0; push_doumail_num=0; ap_v=0,6.0; __utma=30149280.1183179111.1699253418.1699255660.1699271227.3; __utmz=30149280.1699271227.3.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1699271349%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_id.100001.8cb4=be6e56953b997e28.1699271349.; _pk_ses.100001.8cb4=1; __utmt=1; dbcl2="275747579:X+D9PSxlO0U"; ck=BEwq; __utmv=30149280.27574; __utmb=30149280.8.10.1699271227'
}

def assign_none(movie):
    movie = {
    "title": None,
    "year": None,
    "director": None,
    "genre": None,
    "country": None,
    "language": None,
    "release date": None,
    "aka": None,
    "IMDb": None,
    "rating": None,
    "plot": None,
    "cast": None,
    "duration": None,
    "id_recommendations": None
}
    return movie


    
# open the file to read and to save
with open("Movie_id.csv", mode="r", encoding="utf-8") as movielist:
    # read the file
    open("Movies_Philip.json", "w").close()
    csv_reader = csv.reader(movielist)
    cnt=1
    for row in csv_reader:
        time.sleep(1)
        # get the full url
        url_head = "https://movie.douban.com/subject/"
        url_tail = str(row)
        url = url_head + url_tail[2:-2]
        # print(url)
        response = requests.get(url, headers=headers,cookies=cookies)
        soup = BeautifulSoup(response.text, "html.parser")
        # 读取title year director genre rating plot cast duration
        movie["num"] = cnt
        movie["id"] = url_tail[2:-2]
        # title
        title = soup.find("span", attrs={"property": "v:itemreviewed"})
        if title is None:
            movie=assign_none(movie)
            print(str(row) + " is None")
            cnt+=1
            with open("Movies_Philip.json", "a", encoding="utf-8") as json_file:
                json.dump(movie, json_file, indent=4, ensure_ascii=False)
                json_file.write(",\n")
            continue
        else: 
            print(title.text)
            movie["title"] = str(title.text)

        # year
        year = soup.find("span", attrs={"class": "year"})
        print(year.text)

        movie["year"] = (str(year.text))[1:-1]

        # director
        director = soup.find("a", attrs={"rel": "v:directedBy"})
        if director is None:
            movie["director"] = None
        else:
            print(director.text)
            movie["director"] = str(director.text)

        # genre
        genre = soup.find_all("span", attrs={"property": "v:genre"})
        genre_text = [span.text for span in genre]
        print(genre_text)
        movie["genre"] = str(genre_text)

        # country
        country = soup.find("span", attrs={"class": "pl"}, text="制片国家/地区:").next_sibling.strip()
        country_list = country.split("/")
        print(country_list)
        movie["country"] = str(country_list)

        # language
        language = soup.find("span", attrs={"class": "pl"}, text="语言:")
        if language is None:
            movie["language"] = None
        else:
            language_list = language.next_sibling.strip().split("/")
            print(language_list)
            movie["language"] = str(language_list)

        # release date
        release_date = soup.find("span", attrs={"property": "v:initialReleaseDate"})
        if release_date is None:
            movie["release date"] = None
        else:
            print(release_date.text)
            movie["release date"] = str(release_date.text)

        # aka
        aka = soup.find("span", attrs={"class": "pl"}, text="又名:")
        if aka is None:
            movie["aka"] = None
        else :
            aka_list = aka.next_sibling.strip().split("/")
            print(aka_list)
            movie["aka"] = str(aka_list)

        # IMDb
        IMDb = soup.find("span", attrs={"class": "pl"}, text="IMDb:")
        if IMDb is None:
            movie["IMDb"] = None
        else :
            IMDb_list = IMDb.next_sibling.strip()
            print(IMDb_list)
            movie["IMDb"] = str(IMDb_list)

        # rating
        rating = soup.find("strong", attrs={"class": "ll rating_num"})
        if rating is None:
                movie["rating"] = None
        else:
            print(rating.text)
            movie["rating"] = str(rating.text)

        # plot
        plot = soup.find("span", class_="all hidden")
        if plot is not None:
            print(plot.text)
            movie["plot"] = str(plot.text)

        else:
            plot = soup.find("span", attrs={"property": "v:summary"})
            if plot is not None:
                print(plot.text)
                movie["plot"] = str(plot.text)
            else:
                print("Couldn't find intro, whose url=", url_tail)
        # cast
        cast = soup.find_all("a", attrs={"rel": "v:starring"})
        cast = [span.text for span in cast]
        print(cast)

        movie["cast"] = str(cast)

        # duration
        duration = soup.find("span", attrs={"property": "v:runtime"})
        if duration is not None:
            print(duration.text)
            movie["duration"] = str(duration.text)
        else:
            duration=soup.find("span", attrs={"class": "pl"}, text={"单集片长:","片长:"}).next_sibling.strip()
            print(duration)
            movie["duration"] = str(duration)


        # id_recommendations
        patten = r"\d+/"
        recommendations_bd = soup.find("div", attrs={"class": "recommendations-bd"})
        if recommendations_bd is None:
            movie["id_recommendations"] = None
        else:
            dd_tags = recommendations_bd.find_all("dd")
            id_recommendations = []
            # 遍历每个<a>标签，获取其href属性
            for dd_tag in dd_tags:
                a_tag = dd_tag.find("a")
                href = a_tag["href"]
                match = re.search(patten, href)
                if match:
                    id_recommendations.append(match.group()[:-1])
            print(id_recommendations)
            movie["id_recommendations"] = str(id_recommendations)

        cnt+=1
        # save the movie
        with open("Movies_Philip.json", "a", encoding="utf-8") as json_file:
            json.dump(movie, json_file, indent=4, ensure_ascii=False)
            json_file.write(",\n")
