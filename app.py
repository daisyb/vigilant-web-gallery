import urllib2,json
import hashlib
import utils
from flask import Flask, render_template, session, request, redirect, url_for
#from database import *

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    gn = utils.getAllGalleries()
    return render_template("home.html",gallerynames=gn)


@app.route("/gallery/<g>")
def gallery(g):
    if g == None:
        return redirect(url_for("home"))
    elif g in utils.getAllGalleries():
        gn = utils.getAllGalleries()
        return render_template("gallery.html",cgallery=g,gallerynames=gn)
    return redirect(url_for("home"))
    

@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == "GET":
        gn = utils.getAllGalleries()
        return render_template("upload.html",gallerynames=gn)
    else:
        """method which gets stuff from"""
        return redirect(url_for("gallery",g=gallname))

#Temporarily commented out below so that app could run

@app.route("/getimages", methods=['POST'])
def getimages():
    gallery=request.form
    t = gallery.split('/')
    i = len(t) - 1
    while i >= 0:
        if t[i] != None:
            break
        i-=1
    d = utils.getImagePaths(t[i])
    return json.dumps(d)

@app.route("/getthumbnails", methods=['POST'])
def getthumbnails():
    gallery=request.form
    t = gallery.split('/')
    i = len(t) - 1
    while i >= 0:
        if t[i] != None:
            break
        i-=1
    d = utils.getThumbnailPaths(t[i])
    return json.dumps(d)

#@app.route("/getcode", methods=['POST'])
#def getcode():
#    return json.dumps """stuff"""



if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0',port=8001)

