from flask import Flask
from flask import render_template
from flask import request
import re
#from subprocess import call
import subprocess
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    searchFile = open(".searchTerms.txt", "w")
    searchFile.write(text)
    searchFile.close()
    test = open("test", "r")
    #results = call("./resultsServer", stdin=test)
    #urls = results.communicate()
    #print (urls)

    p = subprocess.Popen("./resultsServer", stdin=test, stdout=subprocess.PIPE, shell=True)
    (results,err) = p.communicate()
    print(results)
    results = results.split('\n')
    return render_template("index.html", results=results, numResults = len(results))

if __name__ == "__main__":
    app.run()
