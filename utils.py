# DEPRECATED, NOT USED

import sqlite3
import json
from datetime import date
import PythonMagick
import os, shutil

flask_path = os.path.dirname(__file__) 
database =flask_path + "/imagegallery.db"
image_path = flask_path + "/static/uploads/"

'''
allGalleries:

|   year            | galleryname |   visible     |
|-------------------|-------------|---------------|
|  int (4 digit)    | string      |  int (0 or 1) |

gallery:

|  title  |  path  |
|---------|--------|
| string  | string |
'''

# <---------------------------------------- Helper Functions ---------------------------------------->
def gallery_exists (galleryname):
    con = sqlite3.connect(database)
    cur = con.cursor()
    check_existence = "SELECT CASE WHEN EXISTS ( SELECT * FROM allGalleries WHERE galleryname = '" + galleryname + "' ) THEN CAST(1 AS BIT) ELSE CAST (0 AS BIT) END;"
    return cur.execute(check_existence).fetchall()[0][0]

# <---------------------------------------- Image Manipulation  ---------------------------------------->
def Crop(image, x1, y1, w, h):
    img = PythonMagick.Image(image) # make a copy
    rect = "%sx%s+%s+%s" % (w, h, x1, y1)
    img.crop(rect)
    return img

def Resize(image, w, h):
    img = PythonMagick.Image(image) # copy
    s = "!%sx%s" % (w, h)
    img.sample(s)
    return img


def createThumbnail(imagepath):   #just returns True for now. creates a thumbnail named "thumbnail.png"
    image = PythonMagick.Image(str(imagepath))
    #image = image.write("thumbnail.png")
    geometry = image.size()
    w, h = geometry.width(), geometry.height()
    if (w > h):
        center = w/2
        image = Crop(image, int(center - h/2), 0, h, h)
        #image.crop(int((center - h/2)),  #left
        #           0,               #top
        #           int((center + h/2)),  #right
        #           int(h))               #bottom
    else:
        center = h/2
        image = Crop(image, 0, int(center - w/2), w, w)
        #image.crop(0,                            #left
        #           int((center - w/2)),               #top
        #           int(w),                            #right
        #           int((center + w/2)))               #bottomimage.crop()

    new_size = 175
    image = Resize(image, new_size, new_size)
    #image.resize("{}x{}".format(new_size, new_size))
    #image.resize(new_size, new_size)
    newpath = str(imagepath)[:-9]
    newpath += "thumbnail.png"
    image.write(newpath)
    return True

def limitSize(imagepath):
    print imagepath 
    image = PythonMagick.Image(str(imagepath))
    geometry = image.size()
    w, h = geometry.width(), geometry.height()

    new_size = 1000
    if (w > new_size or h > new_size):
        image = Resize(image, new_size, new_size)
        #image.resize("{}x{}".format(new_size, new_size))
        #image.resize(new_size, new_size)
        image.write(str(imagepath))
    return True

def getSampleImages():  #gets one image from each gallery
    sampledict = []
    glist = getAllGalleries()

    con = sqlite3.connect(database)
    cur = con.cursor()
    for galleryname in glist:
        try:
            sql = "SELECT thumbnailpath FROM "+ galleryname +" where ROWID = 1"
            thumbnailpath = cur.execute(sql).fetchall()[0]   #I may need another [0]
            sampledict.append([galleryname,thumbnailpath])
        except IndexError:
            sampledict.append([galleryname,"images/thluffy-big.png"])
    return sampledict

# <----------------------------------------  Galleries  ---------------------------------------->

def createNewGallery(galleryname):
    '''
    Doing this in a little bit different way. Basically gonna check if gallery exists
    '''
    con = sqlite3.connect(database)
    cur = con.cursor()

    if gallery_exists(galleryname):
        return False
    else:
        sql = "CREATE TABLE IF NOT EXISTS "+ galleryname +"(title TEXT, imagepath TEXT, thumbnailpath TEXT, codepath TEXT)"
        cur.execute(sql)
        currentyear = date.today().year
        sql = "INSERT INTO allGalleries(year, galleryname, visible) VALUES(\"%s\",\"%s\",\"%s\")" % (currentyear, galleryname, 1)
        cur.execute(sql)
        con.commit()
        con.close()
       
        return True
    
def makeGalleriesVisible(year):
    con = sqlite3.connect(database)
    
    cur = con.cursor()
    sql = "UPDATE allGalleries set visible = 1 WHERE year = " + str(year)
    cur.execute(sql)
    con.commit()
    con.close()
    
def makeGalleriesInvisible(year):
    con = sqlite3.connect(database)
    
    cur = con.cursor()
    sql = "UPDATE allGalleries set visible = 0 WHERE year = " + str(year)
    cur.execute(sql)
    con.commit()
    con.close()
    
def getVisibleGalleries():
    con = sqlite3.connect(database)
    cur = con.cursor()
    glist = []
    sql = "SELECT year FROM allGalleries WHERE visible = 1"
    for table in cur.execute(sql).fetchall():
        glist.append(table[0])
    return glist

def getInvisibleGalleries():
    con = sqlite3.connect(database)
    cur = con.cursor()
    glist = []
    sql = "SELECT year FROM allGalleries WHERE visible = 0"
    for table in cur.execute(sql).fetchall():
        glist.append(table[0])
    return glist


def getGallery(galleryname):      #basically gets everything for you, as a list of dictionaries, containing title, imagepath, thumbnailpath, and githublink
    con = sqlite3.connect(database)
    cur = con.cursor()
    gallery = []
    sql = "SELECT * FROM " + galleryname
    for row in cur.execute(sql).fetchall():
        tempdict = {"title" : row[0],
                    "imagepath" : row[1],
                    "thumbnailpath" : row[2],
                    "codepath" : row[3]}
        gallery.append(tempdict)
    con.close()
    return gallery

def getAllGalleries():            #returns a list of the names of all the galleries
    con = sqlite3.connect(database)
    cur = con.cursor()
    glist = []
    sql = "SELECT galleryname FROM allGalleries"
    #sql = "SELECT name FROM sqlite_master WHERE type='table'"
    for table in cur.execute(sql).fetchall():
        glist.append(table[0])
    return glist


def deleteGallery(galleryname):
    if gallery_exists(galleryname):
        con = sqlite3.connect(database)
        cur = con.cursor()
        sql = "DROP TABLE " + galleryname
        cur.execute(sql)
        sql = "DELETE FROM allGalleries WHERE galleryname = '" + galleryname + "'"
        cur.execute(sql)
        con.commit()
        con.close()
        shutil.rmtree(image_path + "/" + galleryname)
        return True
    else:
        return False



# <---------------------------------------- Images ---------------------------------------->
def storeNewImage(galleryname, foldername, uploadername, ispng):      #inserts the info into galleryname table
    con = sqlite3.connect(database)
    cur=con.cursor()
    if ispng:
        imagepath = "uploads" + "/" + galleryname + "/" + foldername + "/image.png"
    else:
        imagepath = "uploads" + "/" + galleryname + "/" + foldername + "/image.gif"
    thumbnailpath = "uploads" + "/" + galleryname + "/" + foldername + "/thumbnail.png"
    codepath = "uploads" + "/" + galleryname + "/" + foldername + "/code.txt"
    sql = "INSERT INTO " + galleryname + "(title, imagepath, thumbnailpath, codepath) VALUES(\"%s\",\"%s\",\"%s\",\"%s\")" % (uploadername, imagepath, thumbnailpath, codepath)
    try:
        cur.execute(sql)
        con.commit()
        con.close()
        #print "worked"
        return True
    except sqlite3.Error as e:
        #print "failed"
        print e
        con.close()
        return False

def getImagePaths(galleryname):
    con = sqlite3.connect(database)
    cur = con.cursor()
    imagepaths = []
    sql = "SELECT imagepath FROM " + galleryname
    for path in cur.execute(sql).fetchall():
        imagepaths.append(path)
    con.close()
    return imagepaths

def getThumbnailPaths(galleryname):
    con = sqlite3.connect(database)
    cur = con.cursor()
    thumbnailpaths = []
    sql = "SELECT thumbnailpath FROM " + galleryname
    for path in cur.execute(sql).fetchall():
        thumbnailpaths.append(path)
    con.close()
    return thumbnailpaths

def deleteImage(galleryname, title):
    if gallery_exists(galleryname):
        con = sqlite3.connect(database)
        cur = con.cursor()
        sql = "SELECT imagepath FROM " + galleryname + " WHERE title = '" + title + "'"
        path = cur.execute(sql).fetchone()[0]
        sql = "DELETE FROM " + galleryname + " WHERE title = '" + title + "'"
        cur.execute(sql)
        con.commit()
        con.close()
        path = path.split("/")
        path.pop()
        path = "/".join(path)
        shutil.rmtree(flask_path + "/static/" + path)
        return True
    return False

def printGalleries(galleryfunct):
	galleries = galleryfunct()
	out = ""
	for index, gallery in enumerate(galleries):
		out = out + str(index) + ": " + gallery[0] + " \n"
	print out

def printAllGalleries():
	printGalleries(getAllGalleries)



def outputJSON():
    out = {}
    galleries = getAllGalleries()
    con = sqlite3.connect(database)
    cur = con.cursor()
    for gallery in galleries:
        sql = "SELECT * FROM " + gallery[0]
        images = cur.execute(sql).fetchall()
        gallery_out = []
        for image in images:
            image_out = {}
            image_out["image_name"] = image[0]
            image_out["image_file"] = image[1]
            image_out["image_thumbnail"] = image[2]
            image_out["image_author"] = image[3]
            gallery_out.append(image_out)
        out[gallery[0]] = gallery_out
    with open('out.json', 'w') as fp:
        json.dump(out, fp)

def loadTestDB():
    galleries = ['picmaker', 'line', 'edge', 'polygon']
    imagenames = ['krzysztofs image', 'daisys image', 'michaels image', 'davids image', 'nicholas image']
    codepath = ['khoch', 'daisyb', 'MGRiv', 'songdavid98', 'NicholasLYang']
    for gallery in galleries:
        createNewGallery(gallery)
        for i in range (0, 5):
            storeNewImage(gallery, imagenames[i], codepath[i])
    
    
