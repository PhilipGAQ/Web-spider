import synonyms
import json

Books_tags = {"title": "无人生还", "tags": ""}
TagList = []
with open("BookTagsDouBan_Philip.json", "+a", encoding="utf-8") as TagJson:
    for line in TagJson:
        data = json.loads(line)
        TagList.append(data)
TagJson.close()
print(TagList)

with open("KeyWords_Philip.json", "+a", encoding="utf-8") as KwJson:
    Books = json.load(KwJson)
    for book in Books:
        Books_tags["title"] = book["title"]
        for keyword in book["keyword"]:
            for tag in TagList:
                 

KwJson.close()
