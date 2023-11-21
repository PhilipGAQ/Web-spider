import synonyms
import json
import re

Movies_tags = {"title": "肖申克的救赎 The Shawshank Redemption",
    "tags": "",
    "id": "1292052"}
TagList = []
with open("MoviesTagDouban.json", "r", encoding="utf-8") as TagJson:
    datas = TagJson.readlines()
    for data in datas:
        TagList.append(data.replace("\n", ""))
TagJson.close()
# print(TagList)


ExpandTag = []
for tag in TagList:
    similar = synonyms.nearby(tag, 5)
    ExpandTag.append(similar[0])
print(ExpandTag)
# bar是接受该关键词的阈值
# bar = 0.89
cnt = 0
with open("TagsForMovies_Philip.json", "w", encoding="utf-8") as TagsJs:
    with open("ResultOfFenciMovie_Philip.json", "r", encoding="utf-8") as KeywordJs:
        Movies = json.load(KeywordJs)
        for movie in Movies:
            TempTags = []
            Movies_tags["title"] = movie["title"]
            Movies_tags["id"]=movie["id"]
            #加入director、country、genre、cast
            TempTags.append(movie["director"])

            countries = movie["country"].strip("[]").replace(" ", "").split(",")
            for country in countries:
                TempTags.append(country.strip("''"))
            
            genres =movie["genre"].strip("[]").replace(" ", "").split(",")
            for genre in genres:
                TempTags.append(genre.strip("''"))

            casts =movie["cast"].strip("[]").replace(" ", "").split(",")
            for cast in casts:
                TempTags.append(cast.strip("''"))


            for keyword in movie["keyword"]:
                for TagGroup in ExpandTag:
                    if keyword in TagGroup:
                        if TagGroup[0] not in TempTags:
                            TempTags.append(TagGroup[0])
                            #print("append")
                """
                for tag in TagList:
                    r = synonyms.compare(tag, keyword, seg=True)
                    if r > bar:
                        # print(r)
                        if tag not in TempTags:
                            TempTags.append(tag)
                """
            Movies_tags["tags"] = TempTags
            json.dump(Movies_tags, TagsJs, indent=4, ensure_ascii=False)
            TagsJs.write(",\n")
            cnt = cnt + 1
            #print(cnt)
