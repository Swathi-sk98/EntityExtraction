from flask import Flask,render_template,url_for,request
import nltk
from nltk.tokenize import sent_tokenize,word_tokenize

input_text = "Sunset is the time of day when our sky meets the outer space solar winds.There are blue, pink,and purple swirls,spinning and twisting,like clouds of balloons caught in a whirlwind.The sun moves slowly to hide behind the line of horizon,while the moon races to take its place in prominence atop the night sky.People slow to a crawl,entranced,fully forgetting the deeds that must still be done.There is a coolness,a calmness,when the sun does set."
tokenized = nltk.sent_tokenize(input_text)


app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/process_content')
def process_content():
    try:    
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)

            namedEnt = r"""NE:{<NN.*>+}"""
            chunkParser = nltk.RegexpParser(namedEnt)
            chunked = chunkParser.parse(tagged)
            return render_template("index.html",results=chunked)
    except Exception as e:
            print(str(e))



if __name__ == '__main__':
    app.run(debug=True)
