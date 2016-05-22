import urllib2,json
import hashlib
import utils
from flask import Flask, render_template, session, request, redirect, url_for
#from database import *

app = Flask(__name__)
gn = ["page1","page2","page3"]


@app.route("/")
@app.route("/home")
@app.route("/menu")
def home():
    gallerynames = getAllGalleries()
    return render_template("home.html",gallerynames=gn)


@app.route("/gallery/<g>")
def gallery(g):
    if g == None:
        return redirect(url_for("home"))
    else:
        cgallery = g
        if g in getAllGalleries():
            gallerynames = getAllGalleries()
    return render_template("gallery.html",cgallery=g,gallerynames=gn)
    

@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == "GET":
        gallerynames = getAllGalleries()
        return render_template("upload.html",gallerynames=gn)
    else:
        """method which gets stuff from"""
        return redirect(url_for("gallery",g=gallname))

#Temporarily commented out below so that app could run

@app.route("/getimages", methods=['POST'])
def getimages():
    d = getImagePaths(gallery)
    return json.dumps(d)

@app.route("/getthumbnails", methods=['POST'])
def getthumbnails():
    d = getThumbnailPaths(galleryname)
    return json.dumps(d)

#@app.route("/getcode", methods=['POST'])
#def getcode():
#    return json.dumps """stuff"""



if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0',port=8001)

