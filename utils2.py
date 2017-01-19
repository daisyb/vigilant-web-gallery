import sqlite3
import json
from datetime import date
#import PythonMagick
import os, shutil

flaskPath = os.path.dirname(__file__)
databasePath = os.path.join(flask_path, "imagegallery2.db")
uploadPath = os.path.join(flask_path, "static/uploads")


'''
Take 2

Basically here's the setup:
One huge table:
| name        |  gallery    | year    |   location           | filetype |  visible     | archived     |
|-------------|-------------|---------|----------------------|----------|--------------|--------------|
| text        | text        | int     |  text                | text     | int (0 or 1) | int (0 or 1) |
| bob's image | line        | 2016    | /2016/line/bobsimage | .png     | 1            |  1           |

'''

# <---------------------- Utils ---------------------->
def screwTuples(shittyTupleList):
    return  [str(i[1]) + i[0] for i in shitty_tuple_list]

def screwTuples2(shittyTupleList):
    return [i[0] for i in shittyTupleList]

def runQuery(query, *args):
    print query
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cursorOutput = cur.execute(query, *args)
    queryOutput = cursorOutput.fetchall()
    con.commit()
    con.close()
    return queryOutput

def setupDB():
    setupImagesTable = """ CREATE TABLE IF NOT EXISTS images
                           (id INTEGER PRIMARY KEY,
                            name TEXT,
                            gallery INTEGER,
                            location TEXT,
                            filetype TEXT);"""
    setupGalleriesTable = """ CREATE TABLE IF NOT EXISTS galleries
                              (id INTEGER PRIMARY KEY,
                               name TEXT,
                               year INTEGER,
                               visible BOOLEAN,
                               archived BOOLEAN);"""

    setupImageGalleriesView = """ CREATE VIEW [images with galleries] AS
                                     SELECT * FROM images AS i
                                     JOIN galleries AS g
                                     ON i.gallery = g.id;"""
    runQuery(setupImagesTable)
    runQuery(setupGalleriesTable)
    runQuery(setupImageGalleriesView)
    if os.path.exists(upload_path):
        shutil.rmtree(upload_path)
    os.makedirs(upload_path)

def reloadDB():
    runQuery("DROP TABLE IF EXISTS images;")
    runQuery("DROP TABLE IF EXISTS galleries;")
    runQuery("DROP VIEW IF EXISTS [images with galleries]")
    setupDB()


def doesGalleryExist (year, galleryName):
    countGalleryQuery = """SELECT COUNT(*) FROM galleries WHERE
                           name = '%s' AND year = %s ;"""
    galleryCount = runQuery(countGalleryQuery % (galleryName, year))[0][0]
    return galleryCount > 0

def doesImageExist (year, galleryName, imageName):
    countImageQuery = """  SELECT COUNT(*) FROM [images with galleries]
                           WHERE name = '%s'
                             AND [name:1] = '%s'
                             AND year = %s;"""
    imageCount = runQuery(countImageQuery % (imageName, galleryName, year))[0][0]
    return imageCount > 0

# <---------------------- Image Tools ---------------------->

def crop(image, x1, y1, w, h):
    img = PythonMagick.Image(image) # make a copy
    rect = "%sx%s+%s+%s" % (w, h, x1, y1)
    img.crop(rect)
    return img

def resize(image, w, h):
    img = PythonMagick.Image(image) # copy
    s = "!%sx%s" % (w, h)
    img.sample(s)
    return img


def createThumbnail(imagePath):   #creates a thumbnail named "thumbnail.png"
    image = PythonMagick.Image(str(imagePath))
    geometry = image.size()
    w, h = geometry.width(), geometry.height()
    if (w > h):
        center = w/2
        image = crop(image, int(center - h/2), 0, h, h)
    else:
        center = h/2
        image = crop(image, 0, int(center - w/2), w, w)

    new_size = 175
    image = resize(image, new_size, new_size)

    newPath = str(imagePath)[:-9]
    newPath += "thumbnail.png"
    image.write(newpath)
    return True

def limitSize(imagePath):
    print imagePath
    image = PythonMagick.Image(str(imagePath))
    geometry = image.size()
    w, h = float(geometry.width()), float(geometry.height())

    new_size = 1000
    if (w > new_size or h > new_size):
        if (w > h):
            image = resize(image, 1000, int(1000 * (h/w)))
        else:
            image = resize(image, int(1000 * (w/h)), 1000)
        image.write(str(imagePath))
    return True

# <---------------------- Images  ---------------------->

def getImagesInGallery(year, galleryName):
    imageQuery = """ SELECT name, location, filetype
                       FROM [images with galleries]
                     WHERE [name:1] = '%s'
                       AND year = %s AND visible = 1"""
    imageQueryOutput = runQuery(imageQuery % (galleryName, year))
    out = []
    for i in imageQueryOutput:
        dict = {}
        dict['title'] = i[0]
        dict['path'] = i[1]
        dict['filetype'] = i[2]
        out.append(dict)
    return out

def getCurrentYearImages(galleryName):
    return getImagesInGallery(date.today().year, gallery)

def insertImage(year, galleryName, imageName, filetype, imagePath):
    # Folder name is different from name cause it has timestamp added
    createGallery(year, galleryName) # If gallery exists will do nothing
    galleryID = getGalleryID(year, galleryName)

    if doesImageExist(year, galleryName, imageName):
        return False

    insertQuery = "INSERT INTO images (name, gallery, location, filetype) VALUES (?, ?, ?, ?)"
    runQuery(insertQuery, (imageName, galleryID, imagePath, filetype))
    return True

def getSampleImages():  #gets one image from each gallery
    sampleImageQuery = """SELECT location FROM [images with galleries]
                           WHERE year = %s GROUP BY gallery;"""
    sampleImages = screwTuples2(runQuery(sampleImageQuery % date.today().year))

def deleteImage(year, galleryName, imageName):
    if doesImageExist(year, galleryName, imageName):
        imageQuery = """SELECT location, [id:1] FROM [images with galleries]
                            WHERE name = '%s' AND [name:1] = '%s' AND year = %s"""
        imageQueryResult = runQuery(imageQuery % (imageName, galleryName, year))[0]
        location = imageQueryResult[0]
        galleryID = imageQueryResult[1]

        deleteQuery= """DELETE FROM images
                          WHERE gallery = ? AND name = ?"""
        runQuery(deleteQuery, (galleryID, imageName))
        try:
            shutil.rmtree(location[3:]) #need to get rid of "../"
        except OSError:
            print "Deleting image with no path"
        return True
    return False


# <---------------------- Galleries  ---------------------->

def getCurrentGalleries():
    galleriesQuery = """SELECT name FROM galleries WHERE
                       archived = 0 AND visible = 1 AND year = %s"""
    return screwTuples2(runQuery(galleriesQuery % date.today().year))

def getAllGalleries():
    galleriesQuery = "SELECT name, year FROM galleries"
    return screwTuples(runQuery(galleriesQuery))

def getGalleriesInYear(year):
    galleriesQuery = "SELECT name FROM galleries WHERE year = '%s'"
    return screwTuples2(runQuery(galleriesQuery % year))

def createGallery(year, galleryName):
    if doesGalleryExist(year, galleryName):
        return False
    else:
        createGalleryQuery = """ INSERT INTO galleries
                                 (name, year, visible, archived)
                                 VALUES
                                 (?, ?, ?, ?) """
        runQuery(createGalleryQuery, (galleryName, year, 1, 0))
        galleryPath = os.path.join(uploadPath, str(year), galleryName)
        if not os.path.exists(galleryPath):
            os.makedirs(galleryPath)
        return True

def getGalleryID(year, galleryName):
     galleryIDQuery = """ SELECT id FROM galleries WHERE
                          year = %s AND name = '%s' """
     return runQuery(galleryIDQuery % (year, galleryName))[0][0]

def setVisibility(year, galleryName, visible):
    visibilityQuery = "UPDATE galleries SET visible = ? WHERE name = ? AND year = ?"
    runQuery(visibilityQuery, (visible, galleryName, year))


def setVisibilityByYear(year, visible):
    visibilityQuery = "UPDATE galleries SET visible = ? WHERE year = ?"
    runQuery(visibilityQuery, (visible, year))

def get_visible_by_year(year):
    visible_query = "SELECT gallery FROM images WHERE year = " + str(year) + " AND visible = 1 AND name = ''"
    return screw_tuples2(run_sql(visible_query))

def get_invisible_by_year(year):
    visible_query = "SELECT gallery FROM images WHERE year = " + str(year) + " AND visible = 0 AND name = ''"
    return screw_tuples2(run_sql(visible_query))

def delete_gallery(year, gallery):
    if gallery_exists(year, gallery):
        delete = "DELETE FROM images WHERE gallery = '" + gallery + "' AND year = " + year
        insert(delete)
        shutil.rmtree(os.path.join(upload_path, year, gallery))
        return True
    return False

def set_archive(year, archive):
    sql = "UPDATE image SET archive = " + str(archive) + "WHERE year = " + year
    insert(sql)

def get_galleries_by_archived(archived):
    sql = "SELECT DISTINCT gallery, year FROM images WHERE archived = " + archived
    sql_out = run_sql(sql)
    out = []
    for gallery in sql_out:
        dict = {}
        dict['gallery'] = gallery[0]
        dict['year'] = gallery[1]
        out.append(dict)
    return out


def get_archived_galleries():
    return get_galleries_by_archived(1)

def get_unarchived_galleries():
    return get_galleries_by_archived(0)



def get_years():
    years_query = "SELECT DISTINCT year FROM images WHERE name = '' "
    years =  screw_tuples2(run_sql(years_query))
    years.sort(reverse = True)
    return years


def get_previous_years():
    years = get_years()
    years.remove(date.today().year)
    return years

def get_invisible_years():
    years_query = "SELECT DISTINCT year FROM images WHERE visible = 0"
    years = screw_tuples2(run_sql(years_query))
    years.sort(reverse = True)
    return years

def get_visible_years():
    years_query = "SELECT DISTINCT year FROM images WHERE visible = 1"
    years =  screw_tuples2(run_sql(years_query))
    years.sort(reverse = True)
    return years
