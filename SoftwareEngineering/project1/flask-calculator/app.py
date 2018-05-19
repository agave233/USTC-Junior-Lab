# -*- coding: utf-8 -*-
from calculate import *
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

@app.route('/_calculate')
def calculate():
    exp = request.args.get('exp')
    try:
        result = count(exp)
    except:
        result = '#'
    return jsonify(result=result)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
