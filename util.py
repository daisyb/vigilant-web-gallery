import sqlite3

def createNewGallery(galleryname):
    con = sqlite3.connect("imagegallery.db")
    
    cur = con.cursor()
    
    sql = "CREATE TABLE IF NOT EXISTS "+ galleryname +"(studentname TEXT, imagename TEXT, filepath TEXT, githublink TEXT)"
    cur.execute(sql)
    
    con.commit()
    con.close()

    
def storeNewImage(galleryname, studentname, imagename, githublink):
    con = sqlite3.connect("imagegallery.db")
    cur=con.cursor()
    filepath = galleryname
    sql = "INSERT INTO " + galleryname + "(studentname, imagename, filepath, githublink) VALUES(\"%s\",\"%s\",\"%s\",\"%s\")" % (studentname, imagename, filepath, githublink)
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
    sql = "SELECT * FROM " + galleryname + " where rowid = filepath"
    for path in cur.execute(sql).fetchall():
        imagepaths.append(path)
    con.close()
    return imagepaths
