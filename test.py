from flask import Flask, render_template,redirect,url_for
from wordcloud import WordCloud, STOPWORDS
import twint
from io import BytesIO
from flask import send_file
from flask import request
import base64

from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request
from transformers import AutoTokenizer, AutoConfig


app = Flask(__name__)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



task='sentiment'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"


import sys
print(sys.path)

from transformers import AutoTokenizer, AutoConfig

#tokenizer = AutoTokenizer.from_pretrained(MODEL)
#config = AutoConfig.from_pretrained(MODEL)

#tokenizer.save_pretrained('woof')
#config.save_pretrained('woof')

#tokenizer = AutoTokenizer.from_pretrained(MODEL)
tokenizer = AutoTokenizer.from_pretrained('twitter-roberta-base-sentiment',
                                config=AutoConfig.from_pretrained('twitter-roberta-base-sentiment'))

    # download label mapping
labels=[]
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode('utf-8').split("\n")
    csvreader = csv.reader(html, delimiter='\t')
labels = [row[1] for row in csvreader if len(row) > 1]

# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
model.save_pretrained(MODEL)

encoded_input = tokenizer(['lol','woof'], return_tensors='pt', padding=True, truncation=True,)
output = model(**encoded_input)
scores = output[0][0].detach().numpy()
scores = softmax(scores)
print(scores)
