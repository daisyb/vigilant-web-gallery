import urllib2,json
import hashlib
import utils
import os
from flask import Flask, render_template, session, request, redirect, url_for
from werkzeug.utils import secure_filename
#from database import *
import uuid
import time

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 #max filesize limit of 10mb

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
        #print request.form
        file = request.files['file']
        gallname = request.form['Gallery']
        code = request.form['code']
        #print gallname
        if file and allowed_file(file.filename): #is a valid file type
            print "is valid file"
            tempname = str(uuid.uuid4())
            temppath = os.path.join('temp',tempname)
            file.save(temppath) #file is saved as temp
            sizeoftemp = os.path.getsize(temppath)
            if sizeoftemp > 10 * 1024 * 1024 and file.filename[-4:] == ".gif":
                print "error" #error message .gif too large
            elif sizeoftemp > 5 * 1024 * 1024 and file.filename[-4:] == ".png":
                print "error" #error message .png too large
            else:
                print "file size is permissible."
            foldername = secure_filename(request.form['name'] + "_" + str(int(time.time()))) #sets foldername to first_last_timestamp
            #print os.path.join(app.config['UPLOAD_FOLDER'], gallname, filename)
            finalpath = os.path.join(app.config['UPLOAD_FOLDER'], gallname, foldername)
            if not os.path.exists(finalpath):
                os.makedirs(finalpath)
            imagepath = os.path.join(app.config['UPLOAD_FOLDER'], gallname, foldername, "image.png")
            os.rename(temppath, imagepath)
            print "file saved"
            utils.storeNewImage(gallname, foldername, request.form['name'])
            print "image stored"
            utils.limitSize(imagepath) #,os.path.join(app.config['UPLOAD_FOLDER'], gallname, foldername, "thumbnail.png"))
            utils.createThumbnail(imagepath)
            print "thumbnail created"
            f = open(os.path.join(app.config['UPLOAD_FOLDER'], gallname, foldername, "code.txt"), 'w')
            f.write(code)
            f.close()
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
                return "success"
    return "Error"

@app.route("/deletegallery/<key>/<gallery>")
def deletegallery(key,gallery):
    if key == "nyang":
        if gallery in utils.getAllGalleries():
            utils.deleteGallery(gallery)
            return "success"
    return "Error"

@app.route("/creategallery/<key>/<gallery>")
def creategallery(key,gallery):
    if key == "nyang":
        if gallery not in utils.getAllGalleries():
            utils.createNewGallery(gallery)
            return "success"
    return "Error"

@app.route("/archivegalleries/<key>/<year>")
def archivegalleries(key,year):
    if key == "nyang":
        utils.makeGalleriesVisible(year)
        return "success"
    return "Error"

@app.route("/unarchivegalleries/<key>/<year>")
def unarchivegalleries(key,year):
    if key == "nyang":
        utils.makeGalleriesInvisible(year)
        return "success"
    return "Error"

#@app.route("/getcode", methods=['POST'])
#def getcode():
#    return json.dumps """stuff"""



if __name__ == "__main__":
    app.debug = True
#    app.run('0.0.0.0',port=8001)
    app.run(host="0.0.0.0")
