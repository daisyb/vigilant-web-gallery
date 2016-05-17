import sqlite3

def createNewGallery(galleryname):
    con = sqlite3.connect("imagegallery.db")
    
    cur = con.cursor()
    
    sql = "CREATE TABLE IF NOT EXISTS "+ galleryname +"(studentname TEXT, imagename TEXT, imagepath TEXT, thumbnailpath TEXT, githublink TEXT)"
    cur.execute(sql)
    
    con.commit()
    con.close()
    
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
    sql = "SELECT * FROM " + galleryname + " where rowid = imagepath"
    for path in cur.execute(sql).fetchall():
        imagepaths.append(path)
    con.close()
    return imagepaths

def getThumbnailPaths(galleryname):
    con = sqlite3.connect("imagegallery.db")
    cur = con.cursor()
    thumbnailpaths = []
    sql = "SELECT * FROM " + galleryname + " where rowid = thumbnailpath"
    for path in cur.execute(sql).fetchall():
        thumbnailpaths.append(path)
    con.close()
    return thumbnailpaths

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
