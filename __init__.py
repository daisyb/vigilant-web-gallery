import urllib2,json
import hashlib
import utils2
import os
import uuid
import time
from datetime import date
from flask import Flask, render_template, session, request, redirect, url_for
from werkzeug.utils import secure_filename

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
@app.route("/<year>/<g>")
@app.route("/<year>")
def gallery(g = None, year = None):
    if year == None:
        gn = utils2.get_current_galleries()
        if g in gn:
            return render_template("gallery.html",cgallery=g,gallerynames=gn)
    else:
        yrs = utils2.get_previous_years()
        yrs = [ format(x,'') for x in yrs ]
        if year not in yrs:
            return redirect(url_for("home"))
        gn = utils2.get_visible_by_year(year)
        if len(gn) == 0:
            return redirect(url_for("home"))
        if g == None:
            g = gn[0]
        return render_template("gallery.html",cgallery=g,gallerynames=gn, yr = year)
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
        if galleryname not in gn:
            return render_template("error.html", error="Stop trying to be clever.")
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

@app.route("/oldgalleries")
def oldgalleries():
    gn = utils2.get_current_galleries()
    y = utils2.get_visible_years()
    return render_template("old.html", gallerynames = gn, years = y)
        
@app.route("/getsamples")
def getsamples():
    d = utils2.get_sample_images()
    return json.dumps(d)


@app.route("/getall", methods=['POST'])
@app.route("/getall/<year>", methods =['POST'])
def getall(year = None):
    gallery = request.form['gallery']
    if year == None:
        d = utils2.get_images_in_gallery(date.today().year, gallery) #this year
    else:
        d = utils2.get_images_in_gallery(year, gallery)
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

@app.route("/getVisibleYears/<key>")
def getVisibleYears(key):
    if key == admin_key:
        gn = utils2.get_visible_years()
        return json.dumps(gn)
    return "Error, invalid key"

@app.route("/getInvisibleYears/<key>")
def getInvisibleYears(key):
    if key == admin_key:
        gn =  utils2.get_invisible_years()
        return json.dumps(gn)
    return "Error, invalid key"
        
@app.route("/getInvisibleGalleries/<key>/")
@app.route("/getInvisibleGalleries/<key>/<year>")
def getInvisibleGalleries(key, year = None):
    if key == admin_key:
        if year == None:
            gn = utils2.get_invisible_by_year(date.today().year)
        else:
            gn = utils2.get_invisible_by_year(year)
        return json.dumps(gn)
    return "Error, invalid key"

@app.route("/getVisibleGalleries/<key>/")
@app.route("/getVisibleGalleries/<key>/<year>")
def getVisibleGalleries(key, year = None):
    if key == admin_key:
        if year == None:
            gn = utils2.get_visible_by_year(date.today().year)
        else:
            gn = utils2.get_visible_by_year(year)
        return json.dumps(gn)
    return "Error, invalid key"

@app.route("/setVisibility/<key>/<visibility>/<gallery>")
@app.route("/setVisibility/<key>/<visibility>/<gallery>/<year>")
def setVisibility(key, visibility, gallery, year = None):
    if key == admin_key:
        if year == None:
            utils2.set_visible(date.today().year,gallery,visibility)
            return "success"
        else:
            utils2.set_visible(year,gallery,visibility)
            return "success"
    return "Error, invalid key"

@app.route("/setVisibilityByYear/<key>/<visibility>")
@app.route("/setVisibilityByYear/<key>/<visibility>/<year>")
def setVisibilityByYear(key, visibility, year = None):
    if key == admin_key:
        if year == None:
            utils2.set_visible_by_year(date.today().year,visibility)
            return "success"
        else:
            utils2.set_visible_by_year(year,visibility)
            return "success"
    return "Error, invalid key"

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
