import urllib2,json
import hashlib
import utils2
import os
from datetime import date
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
upload_path = flask_path + UPLOAD_FOLDER
@app.route("/")
@app.route("/home")
def home():
    gn = utils2.get_current_galleries()
    return render_template("home.html",gallerynames=gn)

@app.route("/gallery/<g>")
def gallery(g):
    if g == None:
        return redirect(url_for("home"))
    elif g in utils2.get_current_galleries():
        gn = utils2.get_current_galleries()
        return render_template("gallery.html",cgallery=g,gallerynames=gn)
    return redirect(url_for("home")) 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == "GET":
        gn = utils2.get_current_galleries()
        return render_template("upload.html", gallerynames=gn, galleries=gn)
    else: 
        #print request.form
        file = request.files['file']
        gallname = request.form['Gallery']
        image_name = " ".join(secure_filename(request.form['name']).split("_"))
        code = request.form['code']
        if image_name == " " or not image_name:
            return render_template("error.html", error="Enter valid image name")
        #print gallname
        if file and allowed_file(file.filename): #is a valid file type
            print "is valid file"
            tempname = str(uuid.uuid4())
            temppath = os.path.join(flask_path, 'temp', tempname)
            file.save(temppath) #file is saved as temp
            sizeoftemp = os.path.getsize(temppath)
            if sizeoftemp > 10 * 1024 * 1024 and file.filename[-4:].lower() == ".gif":
                return render_template("error.html", error="Your file is too large. The maximum allowed file size for a .gif is 10 megabytes.")
            elif sizeoftemp > 5 * 1024 * 1024 and file.filename[-4:].lower() == ".png":
                return render_template("error.html", error="Your file is too large. The maximum allowed file size for a .png is 5 megabytes.")
            else:
                print "File size is acceptable."
            foldername = secure_filename(image_name + "_" + str(int(time.time()))) #sets foldername to first_last_timestamp
            current_year = date.today().year
            relative_image_dir = os.path.join(UPLOAD_FOLDER, str(current_year),  gallname, foldername)

            print "TEMP FILE PATH: "+ temppath
            print "IMAGE DIRECTORY: " + relative_image_dir
            if utils2.add_image(current_year, gallname, image_name,
                                file.filename[-4:].lower(), "../" + relative_image_dir):
                image_dir = os.path.join(flask_path, relative_image_dir)
                os.makedirs(image_dir)
                image_file_path = image_dir + "/image" + file.filename[-4:].lower()
                os.rename(temppath, image_file_path)
                if file.filename[-4:] == ".png":
                    utils2.limit_size(image_file_path)
                utils2.create_thumbnail(image_file_path)
                f = open(image_dir + "/code.txt", 'w')
                f.write(code)
                f.close()
                return redirect(url_for("gallery",g=gallname))
            else:
                return render_template("error.html", error="Failed to write entry to database. An image with the same name likely already exists in that gallery.")
        else:
            return render_template("error.html", error="You did not upload a file or your file name is unacceptable.")

@app.route("/getsamples")
def getsamples():
    d = utils2.get_sample_images()
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
    d = utils2.get_image_paths(t[i])
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
    d = utils2.get_image_paths(t[i])
    return json.dumps(d)

@app.route("/getall", methods=['POST'])
def getall():
    q=request.form
    gallery=q['gallery']
    t = gallery.split('/')
    i = len(t) - 1
    while i >= 0:
        if t[i] != None:
            break
        i-=1
    d = utils2.get_images(t[i])
    print d
    return json.dumps(d)

#API CALLS

@app.route("/getgalleries/<key>")
def getgalleries(key):
    if key == admin_key:
        gn = utils2.get_current_galleries()
        return json.dumps(gn)
    return "Error, invalid key"

@app.route("/getimagename/<key>/<year>/<gallery>")
def getimagename(key, year, gallery):
    if key == admin_key:
        g = utils2.get_images_in_gallery(year, gallery)
        return json.dumps(g)
    return "Error, invalid key"

@app.route("/deleteimage/<key>/<year>/<gallery>/<name>")
def deleteimage(key, year, gallery,name):
    if key == admin_key:
        if utils2.delete_image(year, gallery, name):
            return "success"
        else:
            return "Error, image does not exist"
    return "Error, invalid key"

@app.route("/deletegallery/<key>/<year>/<gallery>")
def deletegallery(key, year, gallery):
    if key == admin_key:
        if utils2.delete_gallery(year, gallery):
            return "success"
        return "Error, gallery does not exist"
    return "Error, invalid key"

@app.route("/creategallery/<key>/<year>/<gallery>")
def creategallery(key, year, gallery):
    if key == admin_key:
        if utils2.add_gallery(year, gallery):
            return "success"
        return "Error, " + gallery + "  already exists"
    return "Error, invalid key"

@app.route("/archivegalleries/<key>/<year>")
def archivegalleries(key,year):
    if key == admin_key:
        return utils2.set_archive(year, 1)
    return "Error, invalid key"

@app.route("/unarchivegalleries/<key>/<year>")
def unarchivegalleries(key,year):
    if key == admin_key:
        return utils2.set_archive(year, 0)
    return "Error"

@app.route("/getInvisibleGalleries/<key>")
def getInvisibleGalleries(key):
    if key == admin_key:
        gn = utils2.get_invisible_galleries()
        return json.dumps(gn)
    return "Error"

@app.route("/getVisibleGalleries/<key>")
def getVisibleGalleries(key):
    if key == admin_key:
        gn = utils2.get_visible_galleries()
        return json.dumps(gn)
    return "Error"

@app.route("/getYears/<key>")
def getYears(key):
    if key == admin_key:
        gn = utils2.get_years()
        return json.dumps(gn)
    return "Error, invalid key"

@app.route("/getGalleriesInYear/<key>/<year>")
def getGalleriesInYear(key,year):
    if key == admin_key:
        gn = utils2.get_galleries_in_year(year)
        return json.dumps(gn)
    return "Error, invalid key"


#@app.route("/getcode", methods=['POST'])
#def getcode():
#    return json.dumps """stuff"""



if __name__ == "__main__":
    app.debug = True
#    app.run('0.0.0.0',port=8001)
    app.run(host="0.0.0.0")
