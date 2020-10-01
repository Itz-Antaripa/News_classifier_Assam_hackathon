from flask import  *
import os , pickle
import json


import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# import nltk
# import warnings
import pickle
import re
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# stop_words = stopwords.words('english')
# from nltk.stem import WordNetLemmatizer

# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics import confusion_matrix, accuracy_score
# import seaborn as sns
# from sklearn.linear_model import LogisticRegression


 
app = Flask(__name__)
app.config['SECRET_KEY'] = '450933c08c5ab75e79619102eddf47dee813a9d6'

# import re
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
 
# from nltk.stem import WordNetLemmatizer
# lemmatizer = WordNetLemmatizer()

import string
from sklearn import *

def clean_text(text):

    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves",
     "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@[A-Za-z]+', '', text)
    text = text.split()
    text = [t for t in text if t not in stop_words]
    text = [t for t in text if t.isalpha()]
    text = ' '.join(text)
    
    return text

     


model = pickle.load(open('model_new.pkl' , 'rb'))
tfidf = pickle.load(open('tfidf1.pkl' , 'rb'))



@app.route("/")
def home():

    return jsonify({
        "msg" : "Fake news detector"
    })
    
@app.route("/detect_page" , methods = ["GET" , "POST"])
def detect_page():
    if(request.method == "POST"):
        name=request.form['formtextarea']
        prediction = model.predict(tfidf.transform([name]))

        if((str(prediction[0])).strip() == "FAKE"):
           
            return render_template("detect_page.html" , text_news = name ,color_gl = "red" ,  glyph_part = "remove-circle" , pred = str(prediction[0])  )
        
        else:
             
            return render_template("detect_page.html" , text_news = name ,  color_gl = "green" ,  glyph_part = "ok-circle" , pred = str(prediction[0])  )        

    
    return "Err.. Try Again"


@app.route("/detect",methods=['GET','POST'])
def detect():

    if(request.method == "POST"):
        query_dat = str(request.args['q'])
        # print(query_dat)
        # print()
        print(clean_text(query_dat))

        prediction = model.predict(tfidf.transform([query_dat]))
        print()
        print(prediction[0])

        return jsonify({
        "msg": str(prediction[0])
        })

    return jsonify({
        "msg": "do a post request with argument as q with the text"
    })


if __name__ == "__main__":
    app.run(port = 5001 , debug= False)

