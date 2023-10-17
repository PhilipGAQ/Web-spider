import json

with open('Books_Philip.json', 'r',encoding="utf-8") as f:
    data = json.load(f)

books={
    "id": "1046265",
    "title": "挪威的森林"
}
with open('Book.json', '+a',encoding="utf-8") as f:
    for book in data:
        books['id']=book["id"]
        books['title']=book['title']
        json.dump(books, f)
        f.write(",\n")
