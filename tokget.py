import nltk


import sys,os
text = open('cv.txt','r').readlines()
tokens = nltk.word_tokenize(str(text))
# Tokenize the text
nltk.download('averaged_perceptron_tagger')

# Part-of-speech tag the tokens
tagged_tokens = nltk.pos_tag(tokens)

filtered_tokens = [token for (token, tag) in tagged_tokens if (len(token) > 2) and ((tag == 'NN') or (tag == 'NNP') or (tag == 'VBG'))]
filtered_tokens = [token.replace('.', '').replace('\\n','').replace('=','') for token in filtered_tokens]
filtered_tokens = [token for token in filtered_tokens if token != '']

ot =open ("tokens.py", "w")
ot.write("STokens = " + str(filtered_tokens))
ot.close()

# ============================== search 
from tokens import STokens
import requests
search = "\'python code\' for creating a file "
url = 'https://www.google.com/search?q=' + search
url = 'https://www.google.com/search?q=%22python+code%22+for+creating+a+file'

#make the request
r = requests.get(url)

#get the response
response = r.text

#print the response
print(response)
