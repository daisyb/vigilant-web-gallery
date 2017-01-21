import filesystem_interface
import sqlite_interface
import time, os
from werkzeug.utils import secure_filename



def validImageName(imageName):
    return not imageName == '' and len(imageName) < 100 and imageName

def validGalleryName(galleryName, galleries):
    return galleryName in galleries


def validImage(imageFile,
               imageName,
               galleryName,
               galleries,
               fileType):
    if not validImageName(imageName):
        imageNameError = """Invalid image name. Names longer than 100 characters
        or left blank will not display properly. Please change it."""
        return imageNameError

    if not validGalleryName(galleryName, galleries):
        return "Stop trying to be clever"

    if not imageFile:
        return "You did not upload a file"

    return True

def create(image, galleries, imageFile, year):
    print "CREATING"
    galleryName = image['Gallery']
    fileName = secure_filename(image['name'])
    imageName = " ".join(fileName.split("_"))
    code = image['code'].encode('ascii', 'ignore')

    fileType = imageFile.filename[-4:].lower()

    imageValid = validImage(imageFile,
                            imageName,
                            galleryName,
                            galleries,
                            fileType)
    print imageValid
    if imageValid != True:
        return imageValid

    print "SAVING"
    folderName = secure_filename(imageName +
                                 "_" +
                                 str(int(time.time())))
    relativeImageDir = os.path.join(str(year),
                                    galleryName,
                                    folderName)

    savedProperly = filesystem_interface.createImage(imageFile,
                                                     imageName,
                                                     year,
                                                     galleryName,
                                                     fileType,
                                                     relativeImageDir,
                                                     code)
    insertedProperly = sqlite_interface.insertImage(year,
                                                    galleryName,
                                                    imageName,
                                                    fileType,
                                                    relativeImageDir)
    if insertedProperly != True:
        location = sqlite_interface.getImageLocation(year,
                                                     galleryName,
                                                     imageName)
        filesystem_interface.deleteImage(location)
        return insertedProperly

    if savedProperly != True:
        print "NOT SAVED PROPERLY"
        sqlite_interface.deleteImage(year, galleryName, imageName)
        return savedProperly

    return True

def delete(location):
    shutil.rmtree(location)
