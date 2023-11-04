# 第一部分：爬虫

## 代码以及解释

以对Movies的爬虫为例：

首先为电影创建一个json字典，方便接下来存储每个电影爬取的信息并write进json文件中

```plain
# 为电影创建一个json字典
movie = {
    "num": "1",  # 电影编号，从1开始
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
    "duration": 142,  # 电影时长（分钟）
    "id_recommendations": ["114514"]
}
```

之后添加反爬虫策略

```plain
# 反爬虫策略
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31"
}
cookies ={
    "Cookie": 'bid=UUJyGxdUAvE; __utmc=30149280; __utmz=30149280.1695283879.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ll="118183"; ap_v=0,6.0; viewed="1046265_1017143_1084336_10466265_2256039_1007305"; apiKey=; dbcl2="274656538:3TdXAga9IPc"; ck=k-Tx; frodotk_db="a537afb8776aee52efa70f296640caf6"; push_noty_num=0; push_doumail_num=0; __utma=30149280.1842746003.1695283879.1695551068.1695556724.6; __utmv=30149280.27465; __utmt_douban=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1695557428%2C%22https%3A%2F%2Fbook.douban.com%2F%22%5D; _pk_id.100001.8cb4=c54a4c010270bb6c.1695557428.; _pk_ses.100001.8cb4=1; __yadk_uid=UW01ZWrMf8VOdGNYSersEnPau2Hod9ry; __utmt=1; __utmb=30149280.26.9.1695557430361'
}
```

根据提供的Movie的id，创建相应的url，之后使用requests库和BeautifulSoup库爬取网页源码

```plain
with open("Movie_id.csv", mode="r", encoding="utf-8") as movielist:
    # read the file
    open("Movies_Philip.json", "w").close()
    csv_reader = csv.reader(movielist)
    cnt=1
    for row in csv_reader:
        # get the full url
        url_head = "https://movie.douban.com/subject/"
        url_tail = str(row)
        url = url_head + url_tail[2:-2]
        # print(url)
        response = requests.get(url, headers=headers,cookies=cookies)
        soup = BeautifulSoup(response.text, "html.parser")
        
```

之后对要爬取的每类信息使用soup.find函数：以title和year的爬取为例：

对 'soup.find()' 函数第一个参数表示要寻找的元素的标签名称，如 'span' 'div' 。第二个参数 'attrs=' 指定要查找的元素的属性的条件，如 'property' 属性指定为 'v:itemreviewed'

之后将movie字典中对应元素赋值即可。

注意：爬取plot时有可能遇见部分隐藏的plot，则首先判断是否有all hidden；爬取tag时应用find_all函数。

```plain
# title
        title = soup.find("span", attrs={"property": "v:itemreviewed"})
        if title is None:
            assign_none(movie)
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
```

最后使用json.dump函数存储在json文件中

```plain
# save the movie
        with open("Movies_Philip.json", "a", encoding="utf-8") as json_file:
            json.dump(movie, json_file, indent=4, ensure_ascii=False)
            json_file.write(",\n")
```

爬虫结果如下：

# 第二部分：检索

## 分词

分词使用到了 'pynlpir' 库。

使用 'pypnlpir.get_key_words' 函数即可对plot进行分词并粗略提取关键词。

```plain
with open("Books_Philip.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)
    for d in data:
        Books_plot["title"] = d["title"]
        Books_plot["writer"]=d["writer"]
        Books_plot["id"]=d["id"]

        if d["plot"] is not None:
            # print(pynlpir.segment(d["plot"], pos_tagging=False))
            print(pynlpir.get_key_words(d["plot"], max_words=50))
            pynlpir.segment(d["plot"])
            Books_plot["keyword"] = pynlpir.get_key_words(d["plot"])
        else:
            Books_plot["keyword"] = ""
        with open("ResultOfFenci_Philip.json", "a", encoding="utf-8") as jf:
            json.dump(Books_plot, jf, indent=4, ensure_ascii=False)
            jf.write(",\n")

```


## 近义词合并

首先爬取豆瓣官网中的tags，来确定最终应该合并到哪些词。

使用 'synonyms.nearby' 函数，对每个官方tag获得5个最相近的近义词，similar[0]为长度为6的以官方tag为首，紧邻5个近义词的list；而ExpandTag为每个元素均为一个list的list。

```plain
ExpandTag = []
for tag in TagList:
    similar = synonyms.nearby(tag, 5)
    ExpandTag.append(similar[0])
```

之后遍历每个分词结果'keyword'，对ExpandTag中的每个TagGroup（包含tag和5个近义词）判断keyword是否出现在该list中，若出现，则将TagGroup的第一个元素（即官方tag）加入该电影或书籍的tag中。此外，我们亦将作者、导演、国家、演员等加入到了电影或数据的tag中。

```plain
            ###上文省略
            for keyword in book["keyword"]:
                for TagGroup in ExpandTag:
                    if keyword in TagGroup:
                        if TagGroup[0] not in TempTags:
                            TempTags.append(TagGroup[0])
```
相比最初的想法，该方法缩小了近义词的比较范围，因此有较好的结果。
最终结果如下：

# 第三部分：推荐系统

## 基本模型训练与测试

我们使用Matrix Factorization算法来对user和item进行推荐预测。

首先加载并处理数据，得到user_ids和item_ids集合，并且创建user/item对index的映射字典。

```plain
#TODO 处理加载的数据，得到item、user和star信息。
#合并相同的userids和itemsids
user_ids=loaded_data["User"].unique()
item_ids=loaded_data["Book"].unique()
#创建user to row的字典
user_to_row ={user_id : idx for idx, user_id in enumerate(user_ids)}
item_to_row ={item_id : idx for idx, item_id in enumerate(item_ids)}
```

创建数据集，建立idx和dataset中的item的映射关系，此处直接将读取的原始数据存入dataset中。

```plain
class RatingDataset(Dataset):
    def __init__(self,data,user_to_row,item_to_row):
        self.data=data
        self.user_to_row=user_to_row
        self.item_to_row=item_to_row

    def __len__(self):
        return len(self.data)

    def __getitem__(self,idx):
        row = self.data.iloc[idx]
        user = self.user_to_row[row['User']]
        book = self.item_to_row[row['Book']]
        rating = row['Rate'].astype('float32')
        return user, book, rating
        
```

创建MatrixFactorize神经网络：初始化将每个user和item分别映射为嵌入向量。forward输出（预测的user对item的评分）为user和item的嵌入向量的点积。

```plain
# embedding_dim为超参数，由用户定义
class MatrixFactorization(nn.Module):
    def __init__(self,num_users,num_books,embedding_dim):
        super(MatrixFactorization,self).__init__()
        #词嵌入技术，将user和item分别嵌入为向量
        self.user_embeddings=nn.Embedding(num_users,embedding_dim)
        self.book_embeddings=nn.Embedding(num_books,embedding_dim)

    def forward(self, user,book):
        # 输出即为user矩阵和book矩阵相乘得到的结果
        user_embedding=self.user_embeddings(user)
        book_embedding=self.book_embeddings(book)
        return (user_embedding*book_embedding).sum(dim=1)
```

以0.5划分训练集和测试集

```plain
#TODO 创建训练集和测试集的数据集对象和数据加载器
train_data, test_data = train_test_split(loaded_data, test_size=0.5, random_state=42)

train_dataset = RatingDataset(train_data, user_to_row, item_to_row)
test_dataset = RatingDataset(test_data, user_to_row, item_to_row)

train_dataloader = DataLoader(train_dataset, batch_size=4096, shuffle=True, drop_last = True)
test_dataloader = DataLoader(test_dataset, batch_size=4096, shuffle=False, drop_last = True)

embedding_dim=32
```

定义loss函数和optimizer函数

```plain
model=MatrixFactorization(num_users,num_books,embedding_dim).to(device)
criterion=nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)
```

以num_epochs进行训练，注意为了防止过拟合现象，loss部分进行了正则化处理。

```plain
model.train()
num_epochs = 10
lambda_b=0.001
lambda_u=0.001
for epoch in range(num_epochs):
    for user, book, rating in train_dataloader:
        optimizer.zero_grad()
        output = model(user, book)
        loss = criterion(output, rating) + lambda_u * model.user_embeddings.weight.norm(2) + lambda_b * model.book_embeddings.weight.norm(2)
        loss.backward()
        optimizer.step()
    # 监控损失或其他性能指标
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}")
```

最后计算testdata的loss，使用余弦相似度计算排序的相似度，并且计算每个user的NDCG

```plain
#部分细节省略
with torch.no_grad():  # 不计算梯度
    for user, book, rating in test_dataloader:
        output = model(user, book)
        loss = criterion(output, rating)
        #print(f"Test Loss: {loss}")
        test_loss += loss.item()

# 计算测试性能指标，例如均方误差或其他指标
average_test_loss = test_loss / len(test_dataloader)
#抽取前100组user
for i in range(num_users):
    #cal ndcg
    ndcg=ndcg_score(real_score_array[i].reshape(1,-1),pred_score_array[i].reshape(1,-1))
    ndcg_sum=ndcg_sum+ndcg
    vec1=np.argsort(real_score_array[i])
    vec2=np.argsort(pred_score_array[i])
    cos_sim = vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    cos_sum=cos_sum+cos_sim
print(f"cos similarity={cossum/100}\nNDCG_score={ndcg_sum/num_users}")
```

## 运行结果：

# 思考：

1. 爬虫部分最开始发现有的plot由于过长，在豆瓣中被“显示全部”所隐藏，因此在源码中有两个部分，一个部分只有未被隐藏的plot，另一部分才有全部的plot。
2. 在近义词合并部分，我们尝试使用'synonyms' 库中的判断两个词的相似度大小的函数'synonyms.compare'，嵌套两个for循环遍历每个分词结果与每个tags判断相近性是否超过0.85，但这样的结果**不尽人意**：首先由于synonyms.compare函数耗时相对较高，导致算法的时间复杂度较高；其次由于'synonyms'库的特性，两个意思相差甚远但属于同一类别的词语可能会有更高的相近性，如“小说”和“科幻小说”。我们最终采用本文档的方法，得到了较好的效果。
3. 矩阵分解算法在训练中发现，对train集具有较好的效果，但对test集loss依然很高，出现了过拟合现象，因此我们对loss部分使用了正则化处理，最终得到了较好的效果。
