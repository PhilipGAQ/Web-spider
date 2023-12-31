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
    "country": ["USA"],
    "language": ["English"],
    "release date":"1994-09-10",
    "aka":"月黑高飞(港)",
    "IMDb":"tt0111161",
    "rating": 9.3,
    "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    "cast": ["Tim Robbins", "Morgan Freeman"],
    "duration": 142,  # 电影时长（分钟）
}

# 反爬虫策略
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31"
}
cookies ={
    "Cookie": 'bid=UUJyGxdUAvE; __utmc=30149280; __utmz=30149280.1695283879.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ll="118183"; ap_v=0,6.0; viewed="1046265_1017143_1084336_10466265_2256039_1007305"; apiKey=; dbcl2="274656538:3TdXAga9IPc"; ck=k-Tx; frodotk_db="a537afb8776aee52efa70f296640caf6"; push_noty_num=0; push_doumail_num=0; __utma=30149280.1842746003.1695283879.1695551068.1695556724.6; __utmv=30149280.27465; __utmt_douban=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1695557428%2C%22https%3A%2F%2Fbook.douban.com%2F%22%5D; _pk_id.100001.8cb4=c54a4c010270bb6c.1695557428.; _pk_ses.100001.8cb4=1; __yadk_uid=UW01ZWrMf8VOdGNYSersEnPau2Hod9ry; __utmt=1; __utmb=30149280.26.9.1695557430361'
}


# open the file to read and to save
with open("Movie_id.csv", mode="r", encoding="utf-8") as movielist:
    # read the file
    csv_reader = csv.reader(movielist)
    for row in csv_reader:
        # get the full url
        url_head = "https://movie.douban.com/subject/"
        url_tail = str(row)
        url = url_head + url_tail[2:-2]
        # print(url)
        response = requests.get(url, headers=headers,cookies=cookies)
        soup = BeautifulSoup(response.text, "html.parser")
        # 读取title year director genre rating plot cast duration

        # title
        title = soup.find("span", attrs={"property": "v:itemreviewed"})
        print(title.text)

        movie["title"] = str(title.text)

        # year
        year = soup.find("span", attrs={"class": "year"})
        print(year.text)

        movie["year"] = (str(year.text))[1:-1]

        # director
        director = soup.find("a", attrs={"rel": "v:directedBy"})
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
        language = soup.find("span", attrs={"class": "pl"}, text="语言:").next_sibling.strip()
        language_list = language.split("/")
        print(language_list)
        movie["language"] = str(language_list)

        # release date
        release_date = soup.find("span", attrs={"property": "v:initialReleaseDate"})
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
        IMDb = soup.find("span", attrs={"class": "pl"}, text="IMDb:").next_sibling.strip()
        print(IMDb)
        movie["IMDb"] = str(IMDb)

        # rating
        rating = soup.find("strong", attrs={"class": "ll rating_num"})
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
            else:
                print("Couldn't find intro, whose url=", url_tail)
        # cast
        cast = soup.find_all("a", attrs={"rel": "v:starring"})
        cast = [span.text for span in cast]
        print(cast)

        movie["cast"] = str(cast)

        # duration
        duration = soup.find("span", attrs={"property": "v:runtime"})
        print(duration.text)
        movie["duration"] = str(duration.text)

        # save the movie
        with open("Movies_Philip.json", "a", encoding="utf-8") as json_file:
            json.dump(movie, json_file, indent=4, ensure_ascii=False)
            json_file.write(",\n")
