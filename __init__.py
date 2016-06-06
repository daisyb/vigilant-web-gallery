import urllib2,json
import hashlib
import utils
import os
from flask import Flask, render_template, session, request, redirect, url_for
from werkzeug.utils import secure_filename
#from database import *

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['txt', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 #max filesize limit of 10mb

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == "GET":
        gn = utils.getAllGalleries()
        return render_template("upload.html", gallerynames=gn, galleries=gn)
    else: 
        print request.form
        #tmp = request.files['file']
        #tmp = tmp.read()
        #print len(tmp)
        file = request.files['file']
        gallname = request.form['Gallery']
        print gallname
        if file and allowed_file(file.filename): #is a valid file type
            print "is valid file"
            foldername = secure_filename(request.form['name'] ) #prevents security exploits
            #print os.path.join(app.config['UPLOAD_FOLDER'], gallname, filename)
            finalpath = os.path.join(app.config['UPLOAD_FOLDER'], gallname, foldername)
            if not os.path.exists(finalpath):
                os.makedirs(finalpath)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], gallname, foldername, "image.png"))
            print "file saved"
            utils.storeNewImage(gallname,foldername)
            print "image stored"
            utils.limitSize(os.path.join(app.config['UPLOAD_FOLDER'], gallname, foldername, "image.png"),os.path.join(app.config['UPLOAD_FOLDER'], gallname, foldername, "thumbnail.png"))
            #utils.createThumbnail(os.path.join(app.config['UPLOAD_FOLDER'], gallname, filename))
            #print "thumbnail created"
            return redirect(url_for("gallery",g=gallname))



@app.route("/getimages", methods=['POST'])
def getimages():
    gallery=request.form[0]
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
    gallery=request.form[0]
    t = gallery.split('/')
    i = len(t) - 1
    while i >= 0:
        if t[i] != None:
            break
        i-=1
    d = utils.getThumbnailPaths(t[i])
    return json.dumps(d)

@app.route("/getall", methods=['POST'])
def getall():
    q=request.form
    gallery=q['gallery']
    print gallery
    t = gallery.split('/')
    i = len(t) - 1
    while i >= 0:
        if t[i] != None:
            break
        i-=1
    d = utils.getGallery(t[i])
    return json.dumps(d)


@app.route("/getgalleries/<key>")
def getgalleries(key):
    if key == "nyang":
        gn = utils.getAllGalleries()
        return json.dumps(gn)
    return "Error"

@app.route("/getimagename/<key>/<name>")
def getimagename(key,name):
    if key == "nyang":
        g = utils.getGallery(name)
        temp = []
        for i in g:
            temp.append(i['title'])
        return json.dumps(temp)
    return "Error"

@app.route("/deleteimage/<key>/<gallery>/<name>")
def deleteimage(key,gallery,name):
    if key == "nyang":
        if gallery in utils.getAllGalleries():
            temp =[]
            for i in g:
                temp.append(i['title'])
            if name in temp:
                utils.deleteImage(gallery,name)
                return redirect(url_for("home"))
    return "Error"

@app.route("/deletegallery/<key>/<gallery>")
def deletegallery(key,gallery):
    if key == "nyang":
        if gallery in utils.getAllGalleries():
            utils.deleteGallery(gallery)
            return redirect(url_for("home"))
    return "Error"

@app.route("/creategallery/<key>/<gallery>")
def creategallery(key,gallery):
    if key == "nyang":
        if gallery not in utils.getAllGalleries():
            utils.createNewGallery(gallery)
            return redirect(url_for("home"))
    return "Error"

@app.route("/archivegalleries/<key>/<year>")
def archivegalleries(key,year):
    if key == "nyang":
        utils.makeGalleriesVisible(year)
        return redirect(url_for("home"))
    return "Error"

@app.route("/unarchivegalleries/<key>/<year>")
def unarchivegalleries(key,year):
    if key == "nyang":
        utils.makeGalleriesInvisible(year)
        return redirect(url_for("home"))
    return "Error"

#@app.route("/getcode", methods=['POST'])
#def getcode():
#    return json.dumps """stuff"""



if __name__ == "__main__":
    app.debug = True
#    app.run('0.0.0.0',port=8001)
    app.run(host="0.0.0.0")
