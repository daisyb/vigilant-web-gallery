import urllib2,json
import hashlib
import utils
import os
from flask import Flask, render_template, session, request, redirect, url_for
from werkzeug.utils import secure_filename
#from database import *

app = Flask(__name__)

UPLOAD_FOLDER = 'galleries/'
ALLOWED_EXTENSIONS = set(['txt', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        print gn
        galleries = ""
        for i in gn:
            print i
            galleries += '<option value="%s">%s</option>' % (i, i)
        print galleries
        return render_template("upload.html", gallerynames=gn, galleries=gn)
    else:
	print request.form
        file = request.files['file']
        #gallname = request.form
        if file and allowed_file(file.filename): #is a valid file type
            filename = secure_filename(file.filename) #prevents security exploits
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + gallname + "/", filename))
            #return redirect(url_for('uploaded_file', filename=filename))
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

@app.route("/getall", methods=['POST'])
def getall():
    gallery=request.form
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
    return

@app.route("/getimagename/<key>/<name>")
def getimagename(key,name):
    if key == "nyang":
        g = utils.getGallery(name)
        temp = []
        for i in g:
            temp.append(i['title'])
        return json.dumps(temp)
    return "Error"

@app.route("/deletion/<key>/<gallery>/<name>")
def deletion(key,gallery,name):
    if key == "nyang":
        pass # Delete stuff
    return "Error"


#@app.route("/getcode", methods=['POST'])
#def getcode():
#    return json.dumps """stuff"""



if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0',port=8001)

