import synonyms

sen1 = "小说"
sen2 = "文学"
# r = synonyms.compare(sen1, sen2, seg=True)
# print(r)
r = synonyms.nearby("小说", 10)
print(r)
print(r[0])
list1 = []
list2 = ["apple", "banana"]
list1.append(r[0])
list1.append(list2)
print(list1)
