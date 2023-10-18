import json

with open("Movies_Philip.json", "r", encoding="utf-8") as f:
    data = json.load(f)

movies = {
    "id": "1292052",
    "title": "肖申克的救赎 The Shawshank Redemption",
}
with open("Movie.json", "+a", encoding="utf-8") as f:
    for movie in data:
        movies["id"] = movie["id"]
        movies["title"] = movie["title"]
        print(movies["title"])
        json.dump(movies, f, indent=4, ensure_ascii=False)
        f.write(",\n")
