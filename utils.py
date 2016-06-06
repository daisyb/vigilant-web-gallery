import sqlite3
import json
from datetime import date
import PythonMagick

def createThumbnail(imagepath):   #just returns True for now. creates a thumbnail named "thumbnail.png"
    image = PythonMagick.Image(str(imagepath))
    geometry = image.size()
    w, h = geometry.width(), geometry.height()
    if (w > h):
        center = w/2
        image.crop(int((center - h/2)),  #left
                   0,               #top
                   int((center + h/2)),  #right
                   int(h))               #bottom
    else:
        center = h/2
        image.crop(0,                            #left
                   int((center - w/2)),               #top
                   int(w),                            #right
                   int((center + w/2)))               #bottomimage.crop()

    new_size = 175
    image.resize("{}x{}".format(new_size, new_size))
    #image.resize(new_size, new_size)
    image.write("thumbnail.png")
    return True

def limitSize(imagepath):
    print imagepath 
    image = PythonMagick.Image(str(imagepath))
    geometry = image.size()
    w, h = geometry.width(), geometry.height()

    new_size = 1000
    if (w > new_size or h > new_size):
        image.resize("{}x{}".format(new_size, new_size))
        #image.resize(new_size, new_size)
    
    image.write("image.png")
    return True

def createNewGallery(galleryname):               #creates a table named galleryname
    con = sqlite3.connect("imagegallery.db")
    
    cur = con.cursor()
    
    sql = "CREATE TABLE IF NOT EXISTS "+ galleryname +"(title TEXT, imagepath TEXT, thumbnailpath TEXT, codepath TEXT)"
    cur.execute(sql)
    currentyear = date.today().year
    sql = "INSERT INTO allGalleries(year, galleryname, visible) VALUES(\"%s\",\"%s\",\"%s\")" % (currentyear, galleryname, 1)
    cur.execute(sql)
    con.commit()
    con.close()

def makeGalleriesVisible(year):
    con = sqlite3.connect("imagegallery.db")
    
    cur = con.cursor()
    sql = "UPDATE allGalleries set visible = 1 where year = " + str(year)
    cur.execute(sql)
    con.commit()
    con.close()
    
def makeGalleriesInvisible(year):
    con = sqlite3.connect("imagegallery.db")
    
    cur = con.cursor()
    sql = "UPDATE allGalleries set visible = 0 where year = " + str(year)
    cur.execute(sql)
    con.commit()
    con.close()
    

def getGallery(galleryname):      #basically gets everything for you, as a list of dictionaries, containing title, imagepath, thumbnailpath, and githublink
    con = sqlite3.connect("imagegallery.db")
    cur = con.cursor()
    gallery = []
    sql = "SELECT * FROM " + galleryname
    for row in cur.execute(sql).fetchall():
        tempdict = {"title" : row[0],
                    "imagepath" : row[1],
                    "thumbnailpath" : row[2],
                    "codepath" : row[3]}
        gallery.append(path)
    con.close()
    return gallery

def getAllGalleries():            #returns a list of the names of all the galleries
    con = sqlite3.connect("imagegallery.db")
    cur = con.cursor()
    glist = []
    #sql = "SELECT galleryname FROM allGalleries"
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    for table in cur.execute(sql).fetchall():
        glist.append(table[0])
    return glist
    
def storeNewImage(galleryname, title):      #inserts the info into galleryname table
    con = sqlite3.connect("imagegallery.db")
    cur=con.cursor()
    imagepath = galleryname + "/" + title + "/image.png"
    thumbnailpath = galleryname + "/" + title + "/thumbnail.png"
    codepath = galleryname + "/" + title + "/code.txt"
    sql = "INSERT INTO " + galleryname + "(title, imagepath, thumbnailpath, code) VALUES(\"%s\",\"%s\",\"%s\",\"%s\")" % (title, imagepath, thumbnailpath, codepath)
    try:
        cur.execute(sql)
        con.commit()
        con.close()
        print "worked"
        return True
    except sqlite3.Error as e:
        print "failed"
        print e
        con.close()
        return False

def getImagePaths(galleryname):
    con = sqlite3.connect("imagegallery.db")
    cur = con.cursor()
    imagepaths = []
    sql = "SELECT imagepath FROM " + galleryname
    for path in cur.execute(sql).fetchall():
        imagepaths.append(path)
    con.close()
    return imagepaths

def getThumbnailPaths(galleryname):
    con = sqlite3.connect("imagegallery.db")
    cur = con.cursor()
    thumbnailpaths = []
    sql = "SELECT thumbnailpath FROM " + galleryname
    for path in cur.execute(sql).fetchall():
        thumbnailpaths.append(path)
    con.close()
    return thumbnailpaths

def deleteImage(galleryname, title):
    con = sqlite3.connect("imagegallery.db")
    cur = con.cursor()
    sql = "DELETE FROM " + galleryname + " WHERE title = " + title
    cur.execute(sql)
    con.commit()
    con.close()
    return True

def deleteGallery(galleryname):
    con = sqlite3.connect("imagegallery.db")
    cur = con.cursor()
    sql = "DROP TABLE " + galleryname
    
    cur.execute(sql)
    con.commit()
    con.close()
    return True




# Just a test function for bash script
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
    con = sqlite3.connect("imagegallery.db")
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
    
    
