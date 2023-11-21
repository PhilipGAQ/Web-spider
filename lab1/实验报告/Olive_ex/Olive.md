### 爬取推荐部分

对豆瓣页面进行分析，

![spider1](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\spider1.png)

推荐的电影网址在<div class = "recommendations-bd">下，目标是读取网页中的书籍id

代码如下

```py
# id_recommendations
        patten = r"\d+/"
        recommendations_bd = soup.find("div", attrs={"class": "recommendations-bd"})
        if recommendations_bd is None:
            movie["id_recommendations"] = None
        else:
            dd_tags = recommendations_bd.find_all("dd")
            id_recommendations = []
            # 遍历每个<a>标签，获取其href属性
            for dd_tag in dd_tags:
                a_tag = dd_tag.find("a")
                href = a_tag["href"]
                match = re.search(patten, href)
                if match:
                    id_recommendations.append(match.group()[:-1])
            print(id_recommendations)
            movie["id_recommendations"] = str(id_recommendations)
```

其中，patten是一个正则表达式，用来匹配数字串，即获取电影id；找到<div class = "recommendations-bd">后，在其下的每一个dd之间找到推荐电影的网址，利用patten匹配找到电影id，将其作为爬取的条目保存。

### 分词部分

分词利用了jieba库

使用jieba.cut将Json文件进行分词，分词过程中只保留中文

```python
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

```

跑出的结果如下：

![](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\jieba.png)

### 索引压缩部分

使用For算法(Frame of Reference)对于建立的倒排表进行压缩，以书籍部分数据为例

首先，建立倒排表，其中，initial_inverted_index保存的是原始倒排表，inverted_index将用于后续的处理

```python
#建立一个字典
inverted_index = defaultdict(list)
initial_inverted_index = defaultdict(list)
for i, doc in enumerate(data):
    for tag in doc['tags']:
        inverted_index[tag].append(i)
# Sort the inverted index by tag
inverted_index = dict(sorted(inverted_index.items()))
initial_inverted_index = copy.deepcopy(inverted_index)
```

原始倒排表 如下：

![compress1](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\compress1.png)

第一步压缩，将倒排表变成差值保存

```python
for key in inverted_index.keys():
    for i in range(len(inverted_index[key])-1,0,-1):
        inverted_index[key][i] = inverted_index[key][i] - inverted_index[key][i-1]
```

差值倒排表如下：

![compress2](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\compress2.png)

对于差值倒排表进行压缩；其中，k的值是指压缩时每一组的元素数量；str_bit是最终压缩成的01串；具体方法为，对于一个倒排表，以k为间隔分组，计算每一组k个数（最后一组可能不足k个）中最大的数需要用几位二进制串表示，即bit_max，由于bit_max最大值不超过1200，1200可以用11位来表示，而11只需要用4位来存储，故用4位存储最大bit长度（str_bit_max = '{:04b}'.format(bit_max)），并将该组所有元素用最大bit长度的01串来表示，然后以01串形式接到str_bit后；由于将01串变为二进制整数存储时会自动去除前导0，为了不让前导0被消除，采用将01串反转再变成二进制整数存储。前导0是第一个分组的最大bit值的一部分，如果丢失会不知道第一个分组的最大bit值（因为最大bit值固定用4比特存储，不知道有几个前导0）。反转后转换成整数，原来的后置0会丢失，但后置0可以通过最后一组的最大bit值计算出来，因为最后一组去除4位最大bit值的长度一定是该组最大bit值的长度的倍数，这一点在后面的解码会体现。

```python
#对于tag差值，进行顺序分组，每组长度为k
#max_temp : 每组中的最大值
#bit_max : max_temp的二进制长度
#str_bit_max : bit_max的二进制串表示
#k的值待定
Compressed_inverted_index = defaultdict(list)
k = 8
for key in inverted_index.keys():
    str_bit = ''
    for i in range(0,len(inverted_index[key]) ,k):
        temp = []
        temp[0:k] = inverted_index[key][i:i+k]
        max_temp = max(temp)
        bit_max = math.ceil(math.log2(max_temp + 1))
        str_bit_max = '{:04b}'.format(bit_max)
        str_bit = str_bit + str_bit_max
        for j in range(0,k):
            if(j < len(temp)):
                str_bit_temp = '{:0{}b}'.format(temp[j],bit_max)
                str_bit = str_bit + str_bit_temp
    #将str_bit反转
    str_bit = str_bit[::-1]
    Compressed_inverted_index[key] = int(str_bit,2)
```

压缩后的倒排表:

![compress3](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\compress3.png)

其中的数据是二进制数据的十进制输出结果

压缩表的解码过程：

```python
#解码Compressed_inverted_index
k = 8
Decompressed_inverted_index = defaultdict(list)
for key in Compressed_inverted_index.keys():
    temp_str = str(bin(Compressed_inverted_index[key])[2:])
    temp_str = temp_str[::-1]
    while(temp_str != ''):
        bit_max = int(temp_str[0:4],2)
        if(bit_max == 0):
            break
        str_todo = temp_str[4:4+ k * bit_max]
        if(len(str_todo) % bit_max != 0):
            str_todo = str_todo + '0' * (bit_max*(int(len(str_todo)/bit_max) + 1) - len(str_todo))
        for i in range(0,len(str_todo),bit_max):
            Decompressed_inverted_index[key].append(int(str_todo[i:i+bit_max],2))
        temp_str = temp_str[4 + k * bit_max:]
#将Decompressed_inverted_index的tag由差值变回原来的值
for key in Decompressed_inverted_index.keys():
    for i in range(1,len(Decompressed_inverted_index[key])):
        Decompressed_inverted_index[key][i] = Decompressed_inverted_index[key][i] + Decompressed_inverted_index[key][i-1]
```

其中，如果待分析的的某一组二进制串去除4位最大bit值后的长度不是最大bit值的倍数，则补上少的0（即在压缩过程中丢失的后置位的0），并进行解压；具体解压方式为，沿着str（01串）进行读取（这里的str已经经过再一次的反转操作将其变为原始的str），最开始读取4位作为第一组的最大bit长度bit_max,然后依次读取k个bit_max长度的内容作为该组的k个元素，这样第一组读完，再读取4位作为第二组的最大bit长度bit_max······依此进行循环，最终解压为初始差值倒排表，再将差值倒排表通过加法操作变成原始倒排表

解压后的倒排表如下：

![compress4](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\compress4.png)

与初始倒排表比较，输出“True",代表解压成功。

```
print(Decompressed_inverted_index == initial_inverted_index)
```

![](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\compress5.png)

### 索引压缩性能测试部分

对于压缩前与压缩后的空间大小进行比较，以书籍的数据为例

```python
for k in range(1,50):
    for key in inverted_index.keys():
        str_bit = ''
        for i in range(0,len(inverted_index[key]) ,k):
            temp = []
            temp[0:k] = inverted_index[key][i:i+k]
            max_temp = max(temp)
            bit_max = math.ceil(math.log2(max_temp + 1))
            str_bit_max = '{:04b}'.format(bit_max)
            str_bit = str_bit + str_bit_max
            for j in range(0,k):
                if(j < len(temp)):
                    str_bit_temp = '{:0{}b}'.format(temp[j],bit_max)
                    str_bit = str_bit + str_bit_temp
        #将str_bit反转
        str_bit = str_bit[::-1]
        Compressed_inverted_index[key] = int(str_bit,2)
    #比较压缩前后的大小
    num_before = 0
    for key in initial_inverted_index.keys():
        num_before += sys.getsizeof(initial_inverted_index[key])
    num_after = 0
    for key in Compressed_inverted_index.keys():
        num_after += sys.getsizeof(Compressed_inverted_index[key])
    print("k = %d, num_before = %d, num_after = %d" % (k,num_before,num_after))
```

输出结果为：

![compress6](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\compress6.png)

由输出结果可知，k = 8时，压缩效果最好，大约减少76.718%的倒排表空间，提升效果显著。

### 社交网络进行推荐部分

在只用score进行训练的代码基础上加入社交网络部分，通过node2vec模型，通过对社交网络组成的图进行随机游走，生成嵌入向量，并与user进行聚合

核心代码如下：

```python
import networkx as nx
G = nx.Graph()
for key, value in contact_sorted.items():
    for v in value:
        G.add_edge(key, v)
node2vec_model = Node2Vec(G, dimensions=200, walk_length=30, num_walks=200, workers=4,temp_folder="D:/temp")
model = node2vec_model.fit(window=10, min_count=1, batch_words=4)
social_embedding_temp = {node : model.wv[node] for node in G.nodes() if node in model.wv}
```

上述代码通过社交关系的集合构建了一个社交关系网络，并定义了一个node2vec模型进行随机游走，生成嵌入向量的集合

```python
class RatingDataset(Dataset):
    def __init__(self,data,user_to_row,item_to_row,social_embedding_dict):
        self.data=data
        self.user_to_row=user_to_row
        self.item_to_row=item_to_row
        self.social_embedding_dict = social_embedding_dict

    def __len__(self):
        return len(self.data)

    def __getitem__(self,idx):
        row = self.data.iloc[idx]
        user = self.user_to_row[row['User']]
        book = self.item_to_row[row['Book']]
        rating = row['Rate'].astype('float32')
        social_embedding = self.social_embedding_dict.get(row['User'], np.zeros(200))
        return user, book, rating,social_embedding
```

上述代码将social_embedding加入到数据中

```python
# embedding_dim为超参数，由用户定义
class MatrixFactorization(nn.Module):
    def __init__(self,num_users,num_books,embedding_dim,hidden_state_social):
        super(MatrixFactorization,self).__init__()
        #词嵌入技术，将user和item分别嵌入为向量
        self.user_embeddings=nn.Embedding(num_users,embedding_dim)
        self.book_embeddings=nn.Embedding(num_books,embedding_dim)
        self.linear_embedding = nn.Linear(hidden_state_social,embedding_dim)
        self.output = nn.Linear(embedding_dim,6)

    def forward(self, user,book,social_embedding):
        # 输出即为user矩阵和book矩阵相乘得到的结果
        user_embedding=self.user_embeddings(user)
        book_embedding=self.book_embeddings(book)
        social_embedding_proj = self.linear_embedding(social_embedding)
        user_intergrate = user_embedding + social_embedding_proj
        return (user_intergrate * book_embedding).sum(dim = 1)
```

上述代码将social_embedding通过隐藏层进行分析，并与user进行聚合

```python
hidden_state_social = 200
model=MatrixFactorization(num_users,num_books,embedding_dim,hidden_state_social).to(device)
criterion=nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)
import numpy as np
model.train()
num_epochs = 20
lambda_b=0.001
lambda_u=0.001
for epoch in range(num_epochs):
    for user, book, rating,social_embedding in train_dataloader:
        optimizer.zero_grad()
        user = user.to(device)
        book = book.to(device)
        rating = rating.to(device)
        social_embedding = social_embedding.float().to(device)
        output = model(user, book,social_embedding)
        loss = criterion(output, rating) + lambda_u * model.user_embeddings.weight.norm(2) + lambda_b * model.book_embeddings.weight.norm(2)
        loss.backward()
        optimizer.step()
    # 监控损失或其他性能指标
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}")
```

上述代码进行训练，并监测loss指标，20次迭代的结果如下：

![](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\social1.png)

平均loss如下：

![social2](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\social2.png)

NDCG如下：

![social3](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\social3.png)