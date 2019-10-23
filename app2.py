from flask import Flask,request,jsonify,render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
import nltk
from nltk.tokenize import sent_tokenize,word_tokenize

app = Flask(__name__)
app.config["MONGO_DBNAME"]= "Entities"
app.config["MONGO_URI"] = "mongodb://localhost:27017/Entities"
mongo = PyMongo(app)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/process_content',methods = ["POST"])
def process_content():
        if request.method == 'POST':
                rawtext = request.form['rawtext']
                newInput = mongo.db.newInput
                input_text = {'name':rawtext}
                
                if newInput.find({'name' : rawtext}).count() <= 0:
                    newInput.insert(input_text)
                

                tokenized = nltk.sent_tokenize(rawtext)
                        
                try:    
                        for i in tokenized:
                            words = nltk.word_tokenize(i)
                            tagged = nltk.pos_tag(words)

                            namedEnt = r"""NE:{<NN.*>+}"""
                            chunkParser = nltk.RegexpParser(namedEnt)
                            chunked = chunkParser.parse(tagged)

                            

                            extractedEntities = mongo.db.extractedEntities

                            results = {'result' : chunked}
                            extractedEntities.insert(results)

                            return render_template("index.html",results=chunked)
                except Exception as e:
                            print(str(e))

                                                         

if __name__ == '__main__':
    app.run(debug=True)
