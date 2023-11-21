import pynlpir
import json

pynlpir.open(encoding_errors="replace")
Books_plot = {"title": "挪威的森林", "keyword": "","writer": "[日]村上春树","id": "1046265"}

with open("ResultOfFenci_Philip.json", "w", encoding="utf-8") as jf:
    jf.write("[")

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

with open("ResultOfFenci_Philip.json", "a", encoding="utf-8") as jf:
    jf.write("]")
pynlpir.close()
