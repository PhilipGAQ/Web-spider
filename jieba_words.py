import json
import jieba

# 读取 JSON 文件
with open('Books_Philip.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 分词
for i in range(0,len(data)):
    title = data[i]['title']
    plot = data[i]['plot']
    if(plot == None):
        continue
    words = jieba.lcut(plot)
    words = [word for word in words if '\u4e00' <= word <= '\u9fa5']  # 只保留中文
    print(i)
    print("\n")
    print(title)
    print(":")
    print(words)
    print("\n")
