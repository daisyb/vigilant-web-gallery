import sqlite3
import json
from datetime import date
#import PythonMagick
import os

flaskPath = os.path.dirname(__file__)
databasePath = os.path.join(flaskPath, "imagegallery.db")

def runQuery(query, *args):
    print query
    con = sqlite3.connect(databasePath)
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

def getImageLocation(year, galleryName, imageName):
    locationQuery = """SELECT location FROM [images with galleries]
                        WHERE year = %s AND [name:1] = '%s' AND
                              name = '%s' """
    return screwTuples2(runQuery(locationQuery % (year,
                                                  galleryName,
                                                  imageName)))
def getCurrentYearImages(galleryName):
    return getImagesInGallery(date.today().year, gallery)

def insertImage(year,
                galleryName,
                imageName,
                fileType,
                imageDir):
    servedImageDir = os.path.join("..", "static", "uploads", imageDir)
    # Folder name is different from name cause it has timestamp added
    createGallery(year, galleryName) # If gallery exists will do nothing
    galleryID = getGalleryID(year, galleryName)

    if doesImageExist(year, galleryName, imageName):
        return """Failed to write entry to database. An image with the
                 same name likely already exists in that gallery."""

    insertQuery = "INSERT INTO images (name, gallery, location, filetype) VALUES (?, ?, ?, ?)"
    runQuery(insertQuery, (imageName, galleryID, servedImageDir, fileType))
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
        return True
    return False


# <---------------------- Galleries  ---------------------->

def getCurrentGalleries():
    galleriesQuery = """SELECT name FROM galleries WHERE
                       archived = 0 AND visible = 1 AND year = %s"""
    return screwTuples2(runQuery(galleriesQuery % date.today().year))

def getAllGalleries():
    galleriesQuery = "SELECT name, year FROM galleries"
    return runQuery(galleriesQuery)

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

def getVisibleByYear(year):
    visibleQuery = "SELECT name FROM galleries WHERE year = %s AND visible = 1"
    return screwTuples2(runQuery(visibleQuery % year))

def getInvisibleByYear(year):
    visibleQuery = "SELECT name FROM galleries WHERE year = %s AND visible = 0"
    return screwTuples2(runQuery(visibleQuery % year))

def deleteGallery(year, galleryName):
    if not doesGalleryExist(year, galleryName):
        return False
    deleteQuery = "DELETE FROM galleries WHERE year = ? AND name = ?"
    runQuery(deleteQuery, (year, galleryName))
    return True

def setArchivedForGallery(year, galleryName, archive):
    archiveQuery = """UPDATE galleries SET archived = ?
                      WHERE name = ? AND year = ?"""
    runQuery(archiveQuery, (archive, galleryName, year))

def setArchivedForYear(year, archive):
    archiveQuery = """UPDATE galleries SET archived = ?
                      WHERE year = ?"""
    runQuery(archiveQuery, (archive, year))


def getGalleriesByArchived(archived):
    archivedQuery = "SELECT name, year FROM galleries WHERE archived = %s"
    queryOutput = runQuery(archivedQuery)
    out = []
    for gallery in queryOutput:
        dict = {}
        dict['gallery'] = gallery[0]
        dict['year'] = gallery[1]
        out.append(dict)
    return out

def getArchivedGalleries():
    return getGalleriesByArchived(1)

def getUnarchivedGalleries():
    return getGalleriesByArchived(0)



def getYears():
    yearsQuery = "SELECT DISTINCT year FROM galleries ORDER BY year DESC"
    years =  screwTuples2(runQuery(yearsQuery))
    return years


def getPreviousYears():
    years = getYears()
    years.remove(date.today().year)
    return years

def getGalleriesByVisibility(visibility):
    yearsQuery = """SELECT name, year FROM galleries
                    WHERE visible = %s ORDER BY year DESC"""
    return screwTuples(runQuery(yearsQuery % visibility))

def getVisibleGalleries():
    return getGalleriesByVisibility(1)

def getInvisibleGalleries():
    return getGalleriesByVisibility(0)

def getYearsByVisibility(visibility):
    yearsQuery = """SELECT DISTINCT year FROM galleries
                    WHERE visible = %s ORDER BY year DESC"""
    years = screwTuples2(runQuery(yearsQuery % visibility))
    if date.today().year in years:
        years.remove(date.today().year)
    return years

def getVisibleYears():
    return getYearsByVisibility(1)

def getInvisibleYears():
    return getYearsByVisibility(0)

# <---------------p------- Utils ---------------------->
def screwTuples(shittyTupleList):
    return  [str(i[1]) + i[0] for i in shittyTupleList]

def screwTuples2(shittyTupleList):
    return [i[0] for i in shittyTupleList]

try:
    setupDB()
except sqlite3.OperationalError:
    print "Already set up db"
