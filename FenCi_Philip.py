import pynlpir
import json

pynlpir.open()
with open("Books_Philip.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)
    print(pynlpir.segment(data[0]["plot"], pos_tagging=False))
    print(pynlpir.get_key_words(data[0]["plot"]))
