import urllib2,json
import hashlib
from flask import Flask, render_template, session, request, redirect, url_for
from database import *

app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/menu")
def home():
    """get gallery names"""
    return render_template("home.html",gallerynames=gn)

@app.route("/gallery")
@app.route("/gallery/<g>")
def gallery():
    if g == None:
        return redirect(url_for("home"))
    else:
        """checks global cgallery for gallery name
        display thumbnails for the galleries
        """
        """not sure if we need this but , gallery=gallery function, thumbnail=thumbnail function,code=code function, name=name function"""
    return render_template("gallery.html",cgallery=g,gallerynames=gn)
    

@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == "GET":
        """get gallery names"""
        return render_template("upload.html",gallerynames=gn)
    else:
        """method which gets stuff from"""
        return redirect(url_for("gallery",g=gallname))


@app.route("/getimages", methods=['POST'])
def getimages():
    return json.dumps """stuff"""

@app.route("/getthumbnails", methods=['POST'])
def getthumbnails():
    return json.dumps """stuff"""

@app.route("/getcode", methods=['POST'])
def getcode():
    return json.dumps """stuff"""
