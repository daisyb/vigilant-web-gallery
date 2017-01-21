import urllib2,json
import hashlib
import sqlite_interface
import image
import os
import urllib
from datetime import date
from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 #max filesize limit of 10mb
flaskPath = os.path.dirname(__file__)
uploadPath = os.path.join(flaskPath, UPLOAD_FOLDER)

secretKeyFile = os.path.join(flaskPath, "secret_key")
adminKey = open(secretKeyFile, 'r') # DO NOT ADD SECRET KEY TO GIT REPO


def setup():
    galleries = sqlite_interface.getAllGalleries()
    for gallery, year in galleries:
        try:
            filesystem_interface.createGallery(year, gallery)
        except:
            print "Files already made"

@app.route("/")
@app.route("/home")
def home():
    galleries = sqlite_interface.getCurrentGalleries()
    return render_template("home.html", galleryNames = galleries)



@app.route("/gallery/<galleryName>")
def currentGallery(galleryName = None):
    galleries = sqlite_interface.getCurrentGalleries()
    if not galleryName in galleries:
        return render_template("error.html",
                               error = "Gallery does not exist")
    return render_template("gallery.html",
                           currentGallery = galleryName,
                           galleryNames = galleries)

@app.route("/<year>")
@app.route("/<year>/<galleryName>")
def previousGallery(year, galleryName = None):
    previousYears =  sqlite_interface.getPreviousYears()
    if int(year) not in previousYears:
        return render_template("error.html", error = "Invalid year")
    galleries = sqlite_interface.getVisibleByYear(year)
    if galleryName == None:
        galleryName = galleries[0]
    return render_template("gallery.html",
                           currentGallery = galleryName,
                           galleryNames = galleries,
                           yr = year)


@app.route("/backfill/<year>",methods=["GET","POST"])
def backfill(year):
    galleries = sqlite_interface.getVisibleByYear(year)
    print "YEAR: " + year
    if request.method == "GET":
        return render_template("upload.html",
                               gallerynames = galleries,
                               galleries = galleries,
                               yr = year)
    else:
        processedProperly = image.create(request.form,
                                     galleries,
                                     request.files['file'],
                                     year)
        if processedProperly != True:
            render_template("error.html",
                            error = processedProperly,
                            galleryNames = galleries)
        return redirect(url_for("previousGallery",
                                galleryName = request.form['Gallery'],
                                year = year))


@app.route("/upload", methods=["GET","POST"])
def upload():
    galleries = sqlite_interface.getCurrentGalleries()
    if request.method == "GET":
        return render_template("upload.html",
                               galleryNames = galleries,
                               galleries = galleries)
    else:
        print "PROCESSING IMAGE"
        processedProperly = image.create(request.form,
                                         galleries,
                                         request.files['file'],
                                         date.today().year)
        print "FINISHED PROCESSING"
        if processedProperly != True:
            render_template("error.html",
                            error = processedProperly,
                            galleryNames = galleries)
        return redirect(url_for("currentGallery", galleryName = request.form['Gallery']))


@app.route("/oldgalleries")
def oldGalleries():
    galleries = sqlite_interface.getCurrentGalleries()
    years = sqlite_interface.getVisibleYears()
    return render_template("old.html",
                           galleryNames = galleries,
                           years = years)

@app.route("/getsamples")
def getsamples():
    d = sqlite_interface.getSampleImages()
    return json.dumps(d)


@app.route("/getall", methods=['POST'])
@app.route("/getall/<year>", methods =['POST'])
def getall(year = None):
    gallery = request.form['gallery']
    if year == None:
        d = sqlite_interface.getImagesInGallery(date.today().year, gallery) #this year
    else:
        d = sqlite_interface.getImagesInGallery(year, gallery)
    print d
    return json.dumps(d)

#API CALLS

@app.route("/getgalleries/<key>")
def getgalleries(key):
    if key == adminKey:
        gn = sqlite_interface.getCurrentGalleries()
        return json.dumps(gn)
    return "Error, invalid key"

@app.route("/getimagename/<key>/<year>/<gallery>")
def getimagename(key, year, gallery):
    if key == adminKey:
        g = sqlite_interface.getImagesInGallery(year, gallery)
        imgnames = []
        for image in g:
            imgnames.append(image['title'])
        return json.dumps(imgnames)
    return "Error, invalid key"

@app.route("/deleteimage/<key>/<year>/<gallery>/<name>")
def deleteimage(key, year, gallery, name):
    name = urllib.unquote_plus(name)
    if key == adminKey:
        if sqlite_interface.deleteImage(year, gallery, name):
            return "success"
        else:
            return "Error, image does not exist"
    return "Error, invalid key"

@app.route("/deletegallery/<key>/<year>/<gallery>")
def deleteGallery(key, year, gallery):
    gallery = urllib.unquote_plus(gallery)
    if key == adminKey:
        if not sqlite_interface.deleteGallery(year, gallery):
            return "Cannot remove gallery from database"
        if not filesystem_interface.deleteGallery(year, gallery):
            return "Cannot delete gallery from filesystem"
        return "Sucess"
    return "Error, invalid key"

@app.route("/creategallery/<key>/<year>/<gallery>")
def createGallery(key, year, gallery):
    gallery = urllib.unquote_plus(gallery)
    if key == adminKey:
        if not sqlite_interface.createGallery(year, gallery):
            return "Error inserting gallery into database"
        if not filesystem_interface.createGallery(year,gallery):
            return "Error creating gallery folder"
        return "Success"
    return "Error, invalid key"

@app.route("/getVisibleYears/<key>")
def getVisibleYears(key):
    if key == adminKey:
        gn = sqlite_interface.getVisibleYears()
        return json.dumps(gn)
    return "Error, invalid key"

@app.route("/getInvisibleYears/<key>")
def getInvisibleYears(key):
    if key == adminKey:
        gn =  sqlite_interface.getInvisibleYears()
        return json.dumps(gn)
    return "Error, invalid key"

@app.route("/getInvisibleGalleries/<key>/")
@app.route("/getInvisibleGalleries/<key>/<year>")
def getInvisibleGalleries(key, year = None):
    if key == adminKey:
        if year == None:
            gn = sqlite_interface.getInvisibleByYear(date.today().year)
        else:
            gn = sqlite_interface.getInvisibleByYear(year)
        return json.dumps(gn)
    return "Error, invalid key"

@app.route("/getVisibleGalleries/<key>/")
@app.route("/getVisibleGalleries/<key>/<year>")
def getVisibleGalleries(key, year = None):
    if key == adminKey:
        if year == None:
            gn = sqlite_interface.getVisibleByYear(date.today().year)
        else:
            gn = sqlite_interface.getVisibleByYear(year)
        return json.dumps(gn)
    return "Error, invalid key"

@app.route("/setVisibility/<key>/<visibility>/<gallery>")
@app.route("/setVisibility/<key>/<visibility>/<gallery>/<year>")
def setVisibility(key, visibility, gallery, year = None):
    gallery = urllib.unquote_plus(gallery)
    if key == adminKey:
        if year == None:
            sqlite_interface.setVisibility(date.today().year,
                                           gallery,
                                           visibility)
            return "success"
        else:
            sqlite_interface.setVisibility(year, gallery, visibility)
            return "success"
    return "Error, invalid key"

@app.route("/setVisibilityByYear/<key>/<visibility>")
@app.route("/setVisibilityByYear/<key>/<visibility>/<year>")
def setVisibilityByYear(key, visibility, year = None):
    if key == adminKey:
        if year == None:
            sqlite_interface.setVisibleByYear(date.today().year,visibility)
            return "success"
        else:
            sqlite_interface.setVisibleByYear(year,visibility)
            return "success"
    return "Error, invalid key"

@app.route("/getYears/<key>")
def getYears(key):
    if key == adminKey:
        gn = sqlite_interface.getYears()
        return json.dumps(gn)
    return "Error, invalid key"

@app.route("/getGalleriesInYear/<key>/<year>")
def getGalleriesInYear(key,year):
    if key == adminKey:
        gn = sqlite_interface.getGalleriesInYear(year)
        return json.dumps(gn)
    return "Error, invalid key"


#@app.route("/getcode", methods=['POST'])
#def getcode():
#    return json.dumps """stuff"""

setup()

if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 8000)
