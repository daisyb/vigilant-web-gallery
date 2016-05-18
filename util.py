import sqlite3

def createNewGallery(galleryname):
    con = sqlite3.connect("imagegallery.db")
    
    cur = con.cursor()
    
    sql = "CREATE TABLE IF NOT EXISTS "+ galleryname +"(studentname TEXT, imagename TEXT, imagepath TEXT, thumbnailpath TEXT, githublink TEXT)"
    cur.execute(sql)
    
    con.commit()
    con.close()

def getGallery(galleryname):      #basically gets everything for you
    con = sqlite3.connect("imagegallery.db")
    cur = con.cursor()
    gallery = []
    sql = "SELECT * FROM " + galleryname
    for row in cur.execute(sql).fetchall():
        tempdict = {"studentname" : row[0],
                    "imagename" : row[1],
                    "imagepath" : row[2],
                    "thumbnailpath" : row[3],
                    "githublink" : row[4]}
        gallery.append(path)
    con.close()
    return gallery

def getAllGalleries():
    con = sqlite3.connect("imagegallery.db")
    cur = con.cursor()
    glist = []
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    for table in cur.execute(sql).fetchall():
        glist.append(table)
    return glist
    
def storeNewImage(galleryname, studentname, imagename,imagepath, thumbnailpath, githublink):
    con = sqlite3.connect("imagegallery.db")
    cur=con.cursor()
    filepath = galleryname
    sql = "INSERT INTO " + galleryname + "(studentname, imagename, imagepath, thumbnailpath, githublink) VALUES(\"%s\",\"%s\",\"%s\",\"%s\")" % (studentname, imagename, imagepath, thumbnailpath, githublink)
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
def testGetGalleries():
	print " Line \n Edge"
