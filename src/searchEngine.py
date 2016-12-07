#!/usr/bin/python2

from flask import Flask
from flask import render_template
from flask import request
import re
import sys
import subprocess

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    search = request.form['search'].lower()
    if len(search) == 0:
        return render_template("index.html", results=None, numResults=0)
    searchFile = open(".searchTerms.txt", "w")
    searchFile.write(search)
    searchFile.close()
    urlText = open(".urlText.txt", "r")

    p = subprocess.Popen("./resultsServer", stdin=urlText, stdout=subprocess.PIPE, shell=True)
    (results,err) = p.communicate()
    results = results.split('\n')
    return render_template("index.html", results=results, numResults = len(results))

if __name__ == "__main__":
    app.run()
