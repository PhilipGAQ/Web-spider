import json
from collections import defaultdict
import math

with open('TagsForBooks_Philip.json', 'r',encoding="utf-8") as f:
    data = json.load(f)

inverted_index = defaultdict(list)

for i, doc in enumerate(data):
    for tag in doc['tags']:
        inverted_index[tag].append(i)

# Sort the inverted index by tag
inverted_index = dict(sorted(inverted_index.items()))

#阈值
threshold = 10

skip_pointers = {}

for tag, docs in inverted_index.items():
    if len(docs) > threshold:
        skip_interval = int(math.sqrt(len(docs)))
        # Create a list of skip pointers
        skip_list = [docs[i:i+skip_interval][-1] for i in range(0, len(docs), skip_interval)]
        skip_pointers[tag] = skip_list

print("Inverted Index:")
print(inverted_index)
print('\n')
print("Skip Pointers:")
print(skip_pointers)
print('\n')