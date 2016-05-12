import urllib2,json
import hashlib
from flask import Flask, render_template, session, request, redirect, url_for
from database import *

app = Flask(__name__)
cgallery = ""

@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
@app.route("/menu",methods=["GET","POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        button = request.form['button']
        if button == "about":
            return redirect(url_for("about"))
        elif button == "home":
            return redirect(url_for("home"))
        else:
            for <blank> in <blank>:
                """Implement a function herer which interates through the list of galleries and returns redirect(url_for("gallery")) and sets a global cgallery to the name of the gallery"""

@app.route("/gallery",methods=["GET","POST"])
def gallery():
    if request.method == "GET":
        """checks global cgallery for gallery name
        if cgallery is null, return to home
        else, display thumbnails for the galleries
        """
    else:
        button = request.form['button']
        if button == "about":
            return redirect(url_for("about"))
        elif button == "home":
            return redirect(url_for("home"))
        else:
            for <blank> in <blank>:
                """see redirect in home"""
