from transformers import BertModel,BertTokenizer
import os

BERT_PATH = './MyBertTokenizer'

tokenizer = BertTokenizer.from_pretrained(BERT_PATH)

print(tokenizer.tokenize('I have a good time, thank you.'))