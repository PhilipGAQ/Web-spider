# 实验二

### 第一阶段 知识图谱子图提取

### 第一跳

第一跳的具体过程：提取douban2fb.txt中的所有电影的MID，将其扩展为实体ID；将这578个实体ID作为第一跳的起点，即在freebase_douban.gz中寻找以这578个实体为头实体的三元组；找到所有三元组后，按照实体20核与关系大于50的条件进行筛选，得到最终的第一跳集合；

提取douban2fb.txt中的所有电影的MID，将其扩展为实体ID：

```python
mapping_file = 'douban2fb.txt'
entity_ids_list = []
with open(mapping_file, 'r') as mapping:
    for line in mapping:
        movie_id, entity_id = line.strip().split()
        entity_id="<http://rdf.freebase.com/ns/" + entity_id+ ">"
        entity_ids_list.append(entity_id)
```

将这578个实体ID作为第一跳的起点，即在freebase_douban.gz中寻找以这578个实体为头实体的三元组，其中，具有str_fault关系的三元组将不被保存；由于该过程跑的时间过长，故将结果保存在文件中，方便后续操作；

```python
str_flag="<http://rdf.freebase.com/ns/"
str_fault="<http://rdf.freebase.com/ns/people.person.date_of_birth>"
with gzip.open('freebase_douban.gz', 'rb') as f, gzip.open('output_first_entity.gz', 'wt') as output1, gzip.open('output_first_3.gz', 'wt') as output2:
    for line in tqdm(f, desc="Processing lines", unit="line"):
        triplet = line.strip().decode().split('\t')[:3]
        if triplet[0] in entity_ids_list and str_flag in triplet[2] and str_fault not in triplet[1]:
            output1.write(triplet[2]+"\n")
            output2.write(triplet[0]+"\t"+triplet[1]+"\t"+triplet[2]+"\n")
```

从文件中提取三元组及其尾实体的集合，保存在first_3和first_jump中；

```python
import gzip
from tqdm import tqdm
first_3 = []#存储第一跳的三元组
first_jump = []#存储第一跳的尾实体
with gzip.open('output_first_entity.gz', 'rb') as f:
    for line in tqdm(f, desc="Processing lines", unit="line"):
        entity = line.strip().decode()
        first_jump.append(entity)
with gzip.open('output_first_3.gz','rb') as f:
    for line in tqdm(f,desc="Processing lines",unit="line"):
        triplet = line.strip().decode().split("\t")[:3]
        first_3.append(triplet)
print(first_3[4])
print(first_jump[4])
```

输出结果为：

![](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\first_1.png)

可以看到，总共有125372个三元组，是第一跳得到的三元组集合，下面开始进行筛选；

```python
#关系<=50则删除，实体<=20则删除
min_relation = 50
min_entity = 20
#函数，通过关系小于50更新first_3，通过first_3更新first_jump
def update_first_3_by_relation (first_3,min_relation,first_jump):
    num_relation = {}#存储每个关系的数量
    num_of_entity = len(first_3)#实体的数量
    for i in range(num_of_entity):
        if first_3[i][1] not in num_relation:
            num_relation[first_3[i][1]] = 1
        else:
            num_relation[first_3[i][1]] = num_relation[first_3[i][1]] + 1
    id_to_delete = []#存储需要删除的三元组的id
    #在first_3中删除关系小于50的三元组,并在first_jump中删除对应的实体
    for i in range(num_of_entity):
        if num_relation[first_3[i][1]] <= min_relation and first_jump[i] not in entity_ids_list:
            id_to_delete.append(i)
    for i in range(len(id_to_delete)):
        del first_3[id_to_delete[i]-i]
        del first_jump[id_to_delete[i]-i]
def update_first_3_by_entity(first_3,min_entity,first_jump):
    num_entity = {}#存储每个实体的数量
    num_of_entity = len(first_3)#实体的数量,即三元组的数量
    for i in range(num_of_entity):
        if first_jump[i] not in num_entity:
            num_entity[first_jump[i]] = 1
        else:
            num_entity[first_jump[i]] = num_entity[first_jump[i]] + 1
    id_to_delete = []#存储需要删除的三元组的id
    #在first_3中删除实体小于20且不在entity_id_list的三元组,并在first_jump中删除对应的实体
    for i in range(num_of_entity):
        if num_entity[first_jump[i]] <= min_entity and first_jump[i] not in entity_ids_list:
            id_to_delete.append(i)
    for i in range(len(id_to_delete)):
        del first_3[id_to_delete[i]-i]
        del first_jump[id_to_delete[i]-i]
#处理第一跳，删除关系小于50的三元组，删除实体小于20的三元组,轮流执行直至first_3和first_jump不再变化
def process_first_jump(first_3,first_jump,min_entity,min_realtion):
    first_3_old = copy.deepcopy(first_3)
    first_jump_old = copy.deepcopy(first_jump)
    i = 0
    print("第"+str(i)+"次处理第一跳")
    print("first_3长度为"+str(len(first_3)))
    i = i + 1
    update_first_3_by_relation(first_3,min_relation,first_jump)
    update_first_3_by_entity(first_3,min_entity,first_jump)
    while first_3_old != first_3 and first_jump_old != first_jump:
        first_3_old = copy.deepcopy(first_3)
        first_jump_old = copy.deepcopy(first_jump)
        print("第"+str(i)+"次处理第一跳")
        print("first_3长度为"+str(len(first_3)))
        i = i + 1
        update_first_3_by_relation(first_3,min_relation,first_jump)
        update_first_3_by_entity(first_3,min_entity,first_jump)
    
process_first_jump(first_3,first_jump,min_entity,min_relation)
```

其中，update_first_3_by_relation 通过判断关系是否达标删除相应的三元组，update_first_3_by_entity通过判断实体是否达标来更新；每一此筛选时，将要删除的先存储在id_to_delete中，之后统一删除；在删除过程中，由于是从first_3的开始到末尾寻找id_to_delete中的进行删除，在删除一个后，其后面的索引值会减一，故删除时应该是del first_3[id_to_delete[i]-i]而不是del first_3[id_to_delete[i]]；在process_first_jump中，轮流执行关系更新与实体更新直至first_3收敛，输出如下：

![](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\first_2.png)

即最终得到的三元组个数为24669个；

对结果进行对错分析：

```python
#测试正确性
num_entity_first_jump = {}
num_relation_first_jump = {}
num_of_entity = len(first_jump)
for i in range(num_of_entity):
    if first_jump[i] not in num_entity_first_jump:
        num_entity_first_jump[first_jump[i]] = 1
    else:
        num_entity_first_jump[first_jump[i]] = num_entity_first_jump[first_jump[i]] + 1
    if first_3[i][1] not in num_relation_first_jump:
        num_relation_first_jump[first_3[i][1]] = 1
    else:
        num_relation_first_jump[first_3[i][1]] = num_relation_first_jump[first_3[i][1]] + 1
min_relation = 50
min_entity = 20
for i in range(num_of_entity):
    if num_entity_first_jump[first_jump[i]] < min_entity and first_jump[i] not in entity_ids_list:
        print("error")
        print(i)
        print(first_jump[i])
    if num_relation_first_jump[first_3[i][1]] < min_relation and first_jump[i] not in entity_ids_list:
        print("error")
        print(i)
        print(first_3[i][1])
print(len(num_entity_first_jump))
print(len(num_relation_first_jump))
```

输出结果为：

![](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\first_3.png)

其中，281为尾实体的种类数（即不完全包含初始的578个），20为关系数量；

统计总的实体数如下：

![first_4](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\first_4.png)

即第一跳的结果为：763个实体，20个关系，24669个三元组；将第一跳的结果写入文件，方便第二跳进行；

#### 第二跳

将第一跳的763个实体作为第二跳的起始实体，通过freebase_douban.gz找到初始三元组集合；与第一跳不同，由于初始三元组集合较大，不能将其存入列表，故先在文件中进行预处理，过滤大于20000的实体与小于50的关系：

在文件中进行删除操作的函数：

```python
def delete_line(line_to_delete):#line_to_delete是一个list,存储了需要删除的行的行号
    with gzip.open('second_3.gz','rb') as second_3:
    #删除line_to_deiete中的对应行，保存在temp_3中
        with gzip.open('temp_3.gz','wt') as output_temp_3:
            line_num = 0
            i = 0
            num_to_delete = len(line_to_delete)
            for line in tqdm(second_3, desc="Processing lines", unit="line"):
                if(line_num != line_to_delete[i]):
                    output_temp_3.write(line.decode())
                else:
                    if(i < num_to_delete - 1):
                        i = i + 1
                line_num = line_num + 1
    print("task1 successfully!")
    #将temp_3中的内容复制到second_3中
    with gzip.open('temp_3.gz','rb') as output_temp_3:
        with gzip.open('second_3.gz','wt') as output_second_3:
            for line in tqdm(output_temp_3, desc="Processing lines", unit="line"):
                output_second_3.write(line.decode())
    print("task2 successfully!")
```

由于文件不能直接删除某一行，，故将不是line_to_delete中的行写入临时文件中，操作完成后再写回second_3.gz

在文件中进行初步筛选的函数：

```python
def update_large(line_to_delete):
    with gzip.open('second_3.gz','rb') as second_3:
        num_entity = {}
        num_relation = {}
        for line in tqdm(second_3, desc="Processing lines", unit="line"):
            triplet = line.decode().strip().split('\t')
            if triplet[2] in num_entity:
                num_entity[triplet[2]] = num_entity[triplet[2]] + 1
            else:
                num_entity[triplet[2]] = 1
            if triplet[0] in num_entity:
                num_entity[triplet[0]] = num_entity[triplet[0]] + 1
            else:
                num_entity[triplet[0]] = 1
            if triplet[1] in num_relation:
                num_relation[triplet[1]] = num_relation[triplet[1]] + 1
            else:
                num_relation[triplet[1]] = 1
        line_number = 0
        second_3.seek(0)
        for line in tqdm(second_3, desc="Processing lines", unit="line"):
            triplet = line.decode().strip().split('\t')
            if num_entity[triplet[2]] > max_entity and triplet[2] not in entity_ids_list:
                line_to_delete.append(line_number)
            elif num_entity[triplet[0]] > max_entity and triplet[0] not in entity_ids_list:
                line_to_delete.append(line_number)
            elif num_relation[triplet[1]] < min_relation:
                line_to_delete.append(line_number)
            line_number = line_number + 1
        print(len(line_to_delete))
```

其中second_3.seek(0)是将文件指针重新指向文件开头；

对文件进行初步筛选：

![](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\second_1.png)

可以看到，初步筛选删除了大部分三元组，剩下745735个三元组，用于后续处理；

现在这745735个三元组可以存入列表second_3中，以类似于第一跳的方式进行处理：

更新函数如下：

```python
min_relation = 50
min_entity = 15
#函数，通过关系小于50更新second_3，通过second_3更新second_jump
def update_second_3_by_relation():
    num_relation = {}#存储每个关系的数量
    num_of_entity = len(second_3)#实体的数量
    for i in range(num_of_entity):
        if second_3[i][1] not in num_relation:
            num_relation[second_3[i][1]] = 1
        else:
            num_relation[second_3[i][1]] = num_relation[second_3[i][1]] + 1
    id_to_delete = []#存储需要删除的三元组的id
    #在second_3中删除关系小于50的三元组,并在second_jump中删除对应的实体
    for i in range(num_of_entity):
        if num_relation[second_3[i][1]] <= min_relation:
            id_to_delete.append(i)
    for i in range(len(id_to_delete)):
        del second_3[id_to_delete[i]-i]
def update_second_3_by_entity():
    num_entity = {}#存储每个实体的数量
    num_of_entity = len(second_3)#实体的数量,即三元组的数量
    for i in range(num_of_entity):
        if second_3[i][0] not in num_entity:
            num_entity[second_3[i][0]] = 1
        else:
            num_entity[second_3[i][0]] = num_entity[second_3[i][0]] + 1
        if second_3[i][2] not in num_entity:
            num_entity[second_3[i][2]] = 1
        else:
            num_entity[second_3[i][2]] = num_entity[second_3[i][2]] + 1
    id_to_delete = []#存储需要删除的三元组的id
    for i in range(num_of_entity):
        if num_entity[second_3[i][0]] <= min_entity and second_3[i][0] in entity_ids_list:
            continue#保护初始三元组
        elif num_entity[second_3[i][0]] <= min_entity and second_3[i][0] not in entity_ids_list:
            id_to_delete.append(i)
        elif num_entity[second_3[i][2]] <= min_entity and second_3[i][2] not in entity_ids_list:
            id_to_delete.append(i)
    for i in range(len(id_to_delete)):
        del second_3[id_to_delete[i]-i]
```

为了保护初始实体，在update_second_3_by_entity中，加入筛选条件，如果一个实体在578个中，且与之相关的三元组数量小于15，则该三元组保留；

对second_3轮流执行上述更新直至收敛：

![](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\second_2.png)

最终得到42387个三元组；

对于代码进行测试：

```python
#测试代码
#测试正确性
num_entity_second_jump = {}
num_relation_second_jump = {}
num_of_entity = len(second_3)
for i in range(num_of_entity):
    if second_3[i][0] not in num_entity_second_jump:
        num_entity_second_jump[second_3[i][0]] = 1
    else:
        num_entity_second_jump[second_3[i][0]] = num_entity_second_jump[second_3[i][0]] + 1
    if second_3[i][2] not in num_entity_second_jump:
        num_entity_second_jump[second_3[i][2]] = 1
    else:
        num_entity_second_jump[second_3[i][2]] = num_entity_second_jump[second_3[i][2]] + 1
    if second_3[i][1] not in num_relation_second_jump:
        num_relation_second_jump[second_3[i][1]] = 1
    else:
        num_relation_second_jump[second_3[i][1]] = num_relation_second_jump[second_3[i][1]] + 1
#测试正确性,测试数量是否符合要求
min_relation = 50
min_entity = 15
for i in range(num_of_entity):
    if num_entity_second_jump[second_3[i][0]] < min_entity and second_3[i][0] in entity_ids_list:
        continue
    elif num_entity_second_jump[second_3[i][0]] < min_entity and second_3[i][0] not in entity_ids_list:
        print("error")
    elif num_entity_second_jump[second_3[i][2]] < min_entity and second_3[i][2] not in entity_ids_list:
        print("error")
    elif num_relation_second_jump[second_3[i][1]] < min_relation:
        print("error")
print(len(num_entity_second_jump))
print(len(num_relation_second_jump))
```

输出结果为：

![](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\second_3.png)

即最终得到1885个实体和24个关系；

将关系写入csv文件：

![second_4](D:\文档\GitHub\Web-spider\实验报告\Olive_ex\second_4.png)

第二跳得到的图谱为：1885个实体，24个关系，42387个三元组；

### 第二阶段第一部分

kg_final.txt的生成：

首先，通过douban2fb.tx与movie_id_map.txt得到初始578个实体ID与最终映射ID的映射关系：

通过second_3.gz得到关系与实体：

```python
entity_list = []
relation_list = []
with gzip.open('second_3.gz','rb') as f:
    for line in tqdm(f,desc="Processing lines", unit="line"):
        triplet = line.strip().decode().split('\t')[:3]
        entity_list.append(triplet[0])
        relation_list.append(triplet[1])
        entity_list.append(triplet[2])
entity_list = list(set(entity_list))
relation_list = list(set(relation_list))
```

对于578个初始实体，获取它们的映射关系：

```python
entity_part2_to_id = {}#实体到id的映射，0-577,即entity_list中的实体到id的映射
movie_id_to_id = {}
with open ('movie_id_map.txt','r') as f:
    for line in f:
        movie_id,entity_id = line.strip().split()
        movie_id_to_id[movie_id] = entity_id
#print(movie_id_to_id)
for entity in entity_ids_list:
    movie_id = ids_to_entity[entity]
    id = movie_id_to_id[movie_id]
    entity_part2_to_id[entity] = int(id)
```

建立剩余的实体的映射关系：

```python
#去除578个初始实体后的所有实体的映射，数值从578开始
#在entity_list中去除entity_ids_list中的实体
i = 578
for entity in entity_list:
    if entity not in entity_ids_list:
        entity_part2_to_id[entity] = i
        i += 1
```

建立关系的映射：

```python
#建立关系的映射
i = 0
relation_to_id = {}
for relation in relation_list:
    relation_to_id[relation] = i
    i += 1
```

将三元组转化为ID三元组：

```python
#将三元组转换为id三元组，利用entity_part2_to_id和relation_to_id
import gzip
from tqdm import tqdm
second_3_id = []
with gzip.open('second_3.gz','rb') as f:
    for line in tqdm(f,desc="Processing lines", unit="line"):
        triplet = line.strip().decode().split('\t')[:3]
		second_3_id.append([entity_part2_to_id[triplet[0]],relation_to_id[triplet[1]],
                    entity_part2_to_id[triplet[2]]])
```

将最终结果存入kg_final.txt

```python
#将id三元组写入文件kg_final.txt
with open('kg_final.txt','w') as f:
    for triplet in second_3_id:
        f.write(str(triplet[0])+' '+str(triplet[1])+' '+str(triplet[2])+'\n')
```



### 遇到的困难：

1.开始处理第二跳时直接将一亿多个三元组存入列表进行处理，导致内存崩溃；之后通过先对文件进行初步筛选解决；

2.开始第二跳结果的数据量过大，通过修改相关筛选条件使最终图谱大小保持在合理值；

3.开始第二跳结果中，某些初始实体（578个中）没有与之对应的三元组，通过加强第二跳对于初始三元组的保护，解决这个问题；

