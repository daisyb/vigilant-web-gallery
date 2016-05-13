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
            galleries = """Implement a function herer which interates through the list of galleries and returns redirect(url_for("gallery")) and sets a global cgallery to the name of the gallery"""
            for gallery in galleries:
                if button == gallery:
                    cgallery = gallery
                    return redirect(url_for(gallery))

@app.route("/gallery",methods=["GET","POST"])
def gallery():
    if request.method == "GET":
        if cgallery == "":
            return redirect(url_for("home"))
        else:
            """checks global cgallery for gallery name
            display thumbnails for the galleries
            """
            """not sure if we need this but , gallery=gallery function, thumbnail=thumbnail function,code=code function, name=name function"""
            return render_template("gallery.html")
    else:
        button = request.form['button']
        if button == "about":
            return redirect(url_for("about"))
        elif button == "home":
            return redirect(url_for("home"))
        else:
            galleries = """Implement a function herer which interates through the list of galleries and returns redirect(url_for("gallery")) and sets a global cgallery to the name of the gallery"""
            for gallery in galleries:
                if button == gallery:
                    cgallery = gallery
                    return redirect(url_for(gallery))

@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    else:
button = request.form['button']
        if button == "about":
            return redirect(url_for("about"))
        elif button == "home":
            return redirect(url_for("home"))
        else:
            galleries = """Implement a function herer which interates through the list of galleries and returns redirect(url_for("gallery")) and sets a global cgallery to the name of the gallery"""
            for gallery in galleries:
                if button == gallery:
                    cgallery = gallery
                    return redirect(url_for(gallery))
