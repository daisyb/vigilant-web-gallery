import sqlite3
import json
#import PythonMagick

def createThumbnail(imagepath):
    image = PythonMagick.Image(imagepath)
    geometry = image.size()
    w, h = geometry.width(), geometry.height()
    square = w                       #length of side of square
    if (w > h):
        square = h
        center = w/2
        image.crop((center - h/2),  #left
                   0,               #top
                   (center + h/2),  #right
                   h)               #bottom
    else:
        center = h/2
        image.crop(0,                            #left
                   (center - w/2),               #top
                   w,                            #right
                   (center + w/2))               #bottomimage.crop()

    new_size = 175
    image.resize("{}x{}".format(new_size, new_size))
    #image.resize(new_size, new_size)
    image.write("thumbnail.png")
    return True

def createNewGallery(galleryname):
    con = sqlite3.connect("imagegallery.db")
    
    cur = con.cursor()
    
    sql = "CREATE TABLE IF NOT EXISTS "+ galleryname +"(title TEXT, imagepath TEXT, thumbnailpath TEXT, githublink TEXT)"
    cur.execute(sql)
    
    con.commit()
    con.close()

def getGallery(galleryname):      #basically gets everything for you, as a list of dictionaries
    con = sqlite3.connect("imagegallery.db")
    cur = con.cursor()
    gallery = []
    sql = "SELECT * FROM " + galleryname
    for row in cur.execute(sql).fetchall():
        tempdict = {"title" : row[0],
                    "imagepath" : row[1],
                    "thumbnailpath" : row[2],
                    "githublink" : row[3]}
        gallery.append(path)
    con.close()
    return gallery

def getAllGalleries():
    con = sqlite3.connect("imagegallery.db")
    cur = con.cursor()
    glist = []
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    for table in cur.execute(sql).fetchall():
        glist.append(table[0])
    return glist
    
def storeNewImage(galleryname, title, githublink):
    con = sqlite3.connect("imagegallery.db")
    cur=con.cursor()
    imagepath = galleryname + "/" + title + "image.png"
    thumbnailpath = galleryname + "/" + title + "thumbnail.png"
    sql = "INSERT INTO " + galleryname + "(title, imagepath, thumbnailpath, githublink) VALUES(\"%s\",\"%s\",\"%s\",\"%s\")" % (title, imagepath, thumbnailpath, githublink)
    try:
        cur.execute(sql)
        con.commit()
        con.close()
        return True
    except sqlite3.Error as e:
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
    github = ['khoch', 'daisyb', 'MGRiv', 'songdavid98', 'NicholasLYang']
    for gallery in galleries:
        createNewGallery(gallery)
        for i in range (0, 5):
            storeNewImage(gallery, imagenames[i], github[i])
    
    
