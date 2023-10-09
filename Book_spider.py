import requests
from bs4 import BeautifulSoup
import re
import csv
import json

# 为书籍创建一个json字典
book = {
    "title": "The little prince",
    "writer": "Antoine de Saint-Exupéry",
    "translator":"马振聘",
    "publisher": "人民文学出版社",
    "date": "2003-8",
    "Original title": "Le Petit Prince",
    "page": 97,
    "price": "22.00元",
    "frame": "平装",
    "rating": 9.1,
    "ISBN": "9787020049294",
    "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    "writer-intro":"安托万·德·圣埃克苏佩里(Antoine de Saint-Exupery, 1900-1944)1900年6月29日出生在法国里昂。他曾经有志于报考海军学院,未能如愿,却有幸成了空军的一员。1923年退役后,先后从事过各种不同的职业。",
    "id_recommendations": ["114514"]

}

# 反爬虫策略
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31"
}
cookies ={
    "Cookie": 'bid=UUJyGxdUAvE; __utmc=30149280; __utmz=30149280.1695283879.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ll="118183"; ap_v=0,6.0; viewed="1046265_1017143_1084336_10466265_2256039_1007305"; apiKey=; dbcl2="274656538:3TdXAga9IPc"; ck=k-Tx; frodotk_db="a537afb8776aee52efa70f296640caf6"; push_noty_num=0; push_doumail_num=0; __utma=30149280.1842746003.1695283879.1695551068.1695556724.6; __utmv=30149280.27465; __utmt_douban=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1695557428%2C%22https%3A%2F%2Fbook.douban.com%2F%22%5D; _pk_id.100001.8cb4=c54a4c010270bb6c.1695557428.; _pk_ses.100001.8cb4=1; __yadk_uid=UW01ZWrMf8VOdGNYSersEnPau2Hod9ry; __utmt=1; __utmb=30149280.26.9.1695557430361'
}

def assign_none(book):
    book={
    "title": None,
    "writer": None,
    "translator":None,
    "publisher": None,
    "date": None,
    "Original title": None,
    "page": None,
    "price": None,
    "frame": None,
    "rating": None,
    "ISBN": None,
    "plot": None,
    "writer-intro":None,
    "id_recommendations": None
    }
    
# open the file to read and to save
with open("Book_id.csv", mode="r", encoding="utf-8") as booklist:
    # read the file
    open("Books_Philip.json", "w").close()
    csv_reader = csv.reader(booklist)
    for row in csv_reader:
        # get the full url
        url_head = "https://book.douban.com/subject/"
        url_tail = str(row)
        url = url_head + url_tail[2:-2]
        # print(url)
        response = requests.get(url, headers=headers,cookies=cookies)
        soup = BeautifulSoup(response.text, "html.parser")
        # 读取title year director genre rating plot cast duration

        # title
        title = soup.find("span", attrs={"property": "v:itemreviewed"})
        if title is None:
            assign_none(book)
            print(str(row) + " is None")
            continue
        else: 
            print(title.text)
            book["title"] = str(title.text)

        # writer
        writer = soup.find("span", attrs={"class": "pl"}, text={"作者"," 作者","作者:"})#作者前的空格不能省略
        if writer is None:
            book["writer"] = None
        else:
            writer = writer.find_next_sibling("a")
            writer_res=writer.text.replace("\n", "").replace(" ","").strip()
            print(writer_res)
            book["writer"] = str(writer_res)

        # translator
        translator = soup.find("span", attrs={"class": "pl"}, text={"译者"," 译者","译者:"})
        if translator is None:
            book["translator"] = None
        else:
            translator = translator.find_next_sibling("a")
            translator_res=translator.text.replace("\n", "").replace(" ","").strip()
            print(translator_res)
            book["translator"] = str(translator_res)
        
        # publisher
        publisher = soup.find("span", attrs={"class": "pl"}, text="出版社:")
        if publisher is None:
            book["publisher"] = None
        else:
            publisher = publisher.find_next_sibling("a")
            if publisher is None:
                publisher = soup.find("span", attrs={"class": "pl"}, text="出版社:").next_sibling.strip()
                print(publisher)
                book["publisher"] = str(publisher)
            else:
                print(publisher.text)
                book["publisher"] = str(publisher.text)

        # date
        date = soup.find("span", attrs={"class": "pl"}, text="出版年:")
        if date is None:
            book["date"] = None
        else:
            date = date.next_sibling.strip()
            print(date)
            book["date"] = str(date)
        
        # Original title
        Original_title = soup.find("span", attrs={"class": "pl"}, text="原作名:")
        if Original_title is None:
            book["Original title"] = None
        else:
            Original_title = Original_title.next_sibling.strip()
            print(Original_title)
            book["Original title"] = str(Original_title)

        # page
        page = soup.find("span", attrs={"class": "pl"}, text="页数:")
        if page is None:
            book["page"] = None
        else:
            page = page.next_sibling.strip()
            print(page)
            book["page"] = str(page)

        # price
        price = soup.find("span", attrs={"class": "pl"}, text="定价:")
        if price is None:
            book["price"] = None
        else:
            price = price.next_sibling.strip()
            print(price)
            book["price"] = str(price)
        
        # frame
        frame = soup.find("span", attrs={"class": "pl"}, text="装帧:")
        if frame is None:
            book["frame"] = None
        else:
            frame = frame.next_sibling.strip()
            print(frame)
            book["frame"] = str(frame)

        # ISBN
        ISBN = soup.find("span", attrs={"class": "pl"}, text="ISBN:")
        if ISBN is None:
            book["ISBN"] = None
        else:
            ISBN = ISBN.next_sibling.strip()
            print(ISBN)
            book["ISBN"] = str(ISBN)

        # rating
        rating = soup.find("strong", attrs={"class": "ll rating_num"})
        if rating is None:
                book["rating"] = None
        else:
            print(rating.text)
            book["rating"] = str(rating.text)

        # plot
        plot_ex=soup.find("div", attrs={"class": "indent", "id": "link-report"})
        if plot_ex is None:
            book["plot"] = None
        else:
            plot = plot_ex.find("span", class_="all hidden")
            if plot is not None:
                print(plot.text)
                book["plot"] = str(plot.text)
            else:
                plot = plot_ex.find("div", class_="intro")
                if plot is not None:
                    print(plot.text)
                    book["plot"] = str(plot.text)
                else:
                    book["plot"] = None
                    print("Couldn't find intro, whose url=", url_tail)

        # writer-intro
        writer_ex = soup.find_all("div", attrs={"class": "indent","id": not"link-report"})
        if writer_ex is None:
            book["writer-intro"] = None
        for ex in writer_ex:
            writer_intro = ex.find("span", class_="all hidden")
            if writer_intro is not None:
                print(writer_intro.text)
                book["writer-intro"] = str(writer_intro.text)
                break
            else:
                writer_intro = ex.find("div", class_="intro")
                if writer_intro is not None:
                    print(writer_intro.text)
                    book["writer-intro"] = str(writer_intro.text)
                    break
        else:
            book["writer-intro"] = None
            print("Couldn't find writer-intro, whose url=", url_tail)

        # save the book
        with open("Books_Philip.json", "a", encoding="utf-8") as json_file:
            json.dump(book, json_file, indent=4, ensure_ascii=False)
            json_file.write(",\n")
