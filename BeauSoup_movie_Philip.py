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
with open("Movie_id.csv", mode="r", encoding="utf-8") as movielist:
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
