import synonyms
import json

Books_tags = {"title": "挪威的森林", "tags": ""}
TagList = []
TagList = []
with open("BookTagsDouBan_Philip.json", "r", encoding="utf-8") as TagJson:
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
with open("TagsForBooks_Philip.json", "w", encoding="utf-8") as TagsJs:
    with open("KeyWords_Philip.json", "r", encoding="utf-8") as KeywordJs:
        Books = json.load(KeywordJs)
        for book in Books:
            TempTags = []
            Books_tags["title"] = book["title"]
            for keyword in book["keyword"]:
                for TagGroup in ExpandTag:
                    if keyword in TagGroup:
                        if TagGroup[0] not in TempTags:
                            TempTags.append(TagGroup[0])
                """
                for tag in TagList:
                    r = synonyms.compare(tag, keyword, seg=True)
                    if r > bar:
                        # print(r)
                        if tag not in TempTags:
                            TempTags.append(tag)
                """
            Books_tags["tags"] = TempTags
            json.dump(Books_tags, TagsJs, indent=4, ensure_ascii=False)
            TagsJs.write(",\n")
            cnt = cnt + 1
            print(cnt)
