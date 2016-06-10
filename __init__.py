import urllib2,json
import hashlib
import utils
import os
from flask import Flask, render_template, session, request, redirect, url_for
from werkzeug.utils import secure_filename
#from database import *
import uuid
import time
admin_key = "mrdwisawesome" # PLEASE CHANGE
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 #max filesize limit of 10mb
flask_path = os.path.dirname(__file__)

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
        if request.form['name'] == " " or not request.form['name']:
            return render_template("error.html", error="Your name cannot be a space.")
        #print gallname
        if file and allowed_file(file.filename): #is a valid file type
            print "is valid file"
            tempname = str(uuid.uuid4())
            temppath = os.path.join(flask_path, 'temp', tempname)
            file.save(temppath) #file is saved as temp
            sizeoftemp = os.path.getsize(temppath)
            if sizeoftemp > 10 * 1024 * 1024 and file.filename[-4:] == ".gif":
                return render_template("error.html", error="Your file is too large. The maximum allowed file size for a .gif is 10 megabytes.")
            elif sizeoftemp > 5 * 1024 * 1024 and file.filename[-4:] == ".png":
                return render_template("error.html", error="Your file is too large. The maximum allowed file size for a .png is 5 megabytes.")
            else:
                print "file size is permissible."
            foldername = secure_filename(request.form['name'] + "_" + str(int(time.time()))) #sets foldername to first_last_timestamp
            #print os.path.join(app.config['UPLOAD_FOLDER'], gallname, filename)
            finalpath = os.path.join(flask_path, app.config['UPLOAD_FOLDER'], gallname, foldername)
            print finalpath
            if not os.path.exists(finalpath):
                os.makedirs(finalpath)
            imagepath = os.path.join(flask_path,app.config['UPLOAD_FOLDER'], gallname, foldername, ("image" + file.filename[-4:]))
            os.rename(temppath, imagepath)
            print "file saved"
            utils.storeNewImage(gallname, foldername, request.form['name'], file.filename[-4:] == ".png")
            print "image stored"
            if file.filename[-4:] == ".png":
                utils.limitSize(imagepath) #,os.path.join(app.config['UPLOAD_FOLDER'], gallname, foldername, "thumbnail.png"))
                utils.createThumbnail(imagepath)
                print "thumbnail created"
            f = open(os.path.join(flask_path, app.config['UPLOAD_FOLDER'], gallname, foldername, "code.txt"), 'w')
            f.write(code)
            f.close()
            return redirect(url_for("gallery",g=gallname))
        else:
            return render_template("error.html", error="You did not upload a file or your file name is unacceptable.")

@app.route("/getsamples")
def getsamples():
    d = utils.getSampleImages()
    return json.dumps(d)


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
    if key == admin_key:
        gn = utils.getAllGalleries()
        return json.dumps(gn)
    return "Error"

@app.route("/getimagename/<key>/<name>")
def getimagename(key,name):
    if key == admin_key:
        g = utils.getGallery(name)
        temp = []
        for i in g:
            temp.append(i['title'])
        return json.dumps(temp)
    return "Error"

@app.route("/deleteimage/<key>/<gallery>/<name>")
def deleteimage(key,gallery,name):
    if key == admin_key:
        if gallery in utils.getAllGalleries():
            g = utils.getGallery(gallery)
            temp =[]
            for i in g:
                temp.append(i['title'])
            if name in temp:
                utils.deleteImage(gallery,name)
                return "success"
    return "Error"

@app.route("/deletegallery/<key>/<gallery>")
def deletegallery(key,gallery):
    if key == admin_key:
        if gallery in utils.getAllGalleries():
            utils.deleteGallery(gallery)
            return "success"
    return "Error"

@app.route("/creategallery/<key>/<gallery>")
def creategallery(key,gallery):
    if key == admin_key:
        if gallery not in utils.getAllGalleries():
            utils.createNewGallery(gallery)
            return "success"
    return "Error"

@app.route("/archivegalleries/<key>/<year>")
def archivegalleries(key,year):
    if key == admin_key:
        utils.makeGalleriesVisible(year)
        return "success"
    return "Error"

@app.route("/unarchivegalleries/<key>/<year>")
def unarchivegalleries(key,year):
    if key == admin_key:
        utils.makeGalleriesInvisible(year)
        return "success"
    return "Error"

@app.route("/getInvisibleGalleries/<key>")
def getInvisibleGalleries(key):
    if key == admin_key:
        gn = utils.getInvisibleGalleries()
        return json.dumps(gn)
    return "Error"

@app.route("/getVisibleGalleries/<key>")
def getVisibleGalleries(key):
    if key == admin_key:
        gn = utils.getVisibleGalleries()
        return json.dumps(gn)
    return "Error"

#@app.route("/getcode", methods=['POST'])
#def getcode():
#    return json.dumps """stuff"""



if __name__ == "__main__":
    app.debug = True
#    app.run('0.0.0.0',port=8001)
    app.run(host="0.0.0.0")
