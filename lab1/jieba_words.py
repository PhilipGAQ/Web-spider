import json
import jieba

# 读取 JSON 文件
with open('Books_Philip.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

book_words = {
    "num": "1",
    "title": "The little prince",
    "writer": "Antoine de Saint-Exupéry",
    "words": ["一"]
}


# 分词
for i in range(0,len(data)):
    title = data[i]['title']
    book_words["title"] = title
    writer = data[i]['writer']
    book_words["writer"] = writer
    book_words["num"] = i
    plot = data[i]['plot']
    if(plot == None):
        continue
    words = jieba.lcut(plot)
    words = [word for word in words if '\u4e00' <= word <= '\u9fa5']  # 只保留中文
    book_words["words"] = words  # 将分词结果拼接成一个字符串
    with open("book_jieba_words.json", "a", encoding="utf-8") as json_file:
        json.dump(book_words, json_file, indent=4, ensure_ascii=False)

