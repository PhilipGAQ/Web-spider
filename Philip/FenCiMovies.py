import pynlpir
import json

pynlpir.open(encoding_errors="replace")

Movies_plot = {"title": "肖申克的救赎 The Shawshank Redemption",
 "director": "弗兰克·德拉邦特",
 "id": "1292052",
 "country": "['美国']",
 "genre": "['剧情', '爱情']",
 "cast": "['蒂姆·罗宾斯', '摩根·弗里曼', '鲍勃·冈顿', '威廉姆·赛德勒', '克兰西·布朗', '吉尔·贝罗斯', '马克·罗斯顿', '詹姆斯·惠特摩', '杰弗里·德曼', '拉里·布兰登伯格', '尼尔·吉恩托利', '布赖恩·利比', '大卫·普罗瓦尔', '约瑟夫·劳格诺', '祖德·塞克利拉', '保罗·麦克兰尼', '芮妮·布莱恩', '阿方索·弗里曼', 'V·J·福斯特', '弗兰克·梅德拉诺', '马克·迈尔斯', '尼尔·萨默斯', '耐德·巴拉米', '布赖恩·戴拉特', '唐·麦克马纳斯']",
  "keyword": ""}


#保留所有的原始信息，等到syn时再进行处理。
'''
with open("Movies_Philip.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)
    for d in data:
        tags = d["genre"].strip("[]").replace(" ", "").split(",")
        for tag in tags:
            print(tag)
'''
#仅将plot进行分词并加入到keyword中即可

with open("ResultOfFenciMovie_Philip.json", "w", encoding="utf-8") as jf:
    jf.write("[")

with open("Movies_Philip.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)
    for d in data:
        Movies_plot["title"]=d["title"]
        Movies_plot["director"]=d["director"]
        Movies_plot["id"]=d["id"]
        Movies_plot["country"]=d["country"]
        Movies_plot["genre"]=d["genre"]
        Movies_plot["cast"]=d["cast"]

        if d["plot"] is not None:
            # print(pynlpir.segment(d["plot"], pos_tagging=False))
            print(pynlpir.get_key_words(d["plot"], max_words=50))
            pynlpir.segment(d["plot"])
            Movies_plot["keyword"] = pynlpir.get_key_words(d["plot"])
        else:
            Movies_plot["keyword"] = ""
        with open("ResultOfFenciMovie_Philip.json", "a", encoding="utf-8") as jf:
            json.dump(Movies_plot, jf, indent=4, ensure_ascii=False)
            jf.write(",\n")

with open("ResultOfFenciMovie_Philip.json", "a", encoding="utf-8") as jf:
    jf.write("]")
    
pynlpir.close()
