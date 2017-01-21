import os, uuid, shutil
import image_utils


ALLOWED_EXTENSIONS = set(['png', 'gif'])


flaskPath = os.path.dirname(__file__)
uploadPath = os.path.join(flaskPath, "uploads")

try:
    os.symlink(uploadPath, os.path.join(flaskPath, "static", "uploads"))
except OSError:
    print "Already symlinked"


def validGIF(tempSize):
    return tempSize < 10 * 1024 * 1024

def validPNG(tempSize):
    return tempSize < 5 * 1024 * 1024

def validFile(tempSize, fileType):
    if fileType == ".gif":
        if not validGIF(tempSize):
            return """Your file is too large. The maximum allowed file
            size for a .gif is 10 megabytes."""
        return True
    elif fileType == ".png":
        if not validPNG(tempSize):
            return """Your file is too large. The maximum allowed file
                  size for a .png is 5 megabytes."""
        return True
    return "Invalid file type"

def createImage(imageFile,
                imageName,
                year,
                galleryName,
                fileType,
                relativeImageDir,
                code):

    tempName = str(uuid.uuid4())
    tempPath = os.path.join(flaskPath, 'temp', tempName)
    imageFile.save(tempPath) #file is saved as temp
    tempSize = os.path.getsize(tempPath)
    fileValid = validFile(tempSize, fileType)
    if fileValid != True:
        return fileValid

    #sets foldername to first_last_timestamp
    imageDir = os.path.join(flaskPath, relativeImageDir)
    os.makedirs(imageDir)
    print "Made directory: " + imageDir
    imageFilePath = os.path.join(imageDir,
                                 "image" + fileType)
    os.rename(tempPath, imageFilePath)
    f = open(os.path.join(imageDir + "code.txt"), 'w')
    f.write(code)
    f.close()
    shutil.rmtree(os.path.join(flaskPath, "temp"))
    os.makedirs(os.path.join(flaskPath, "temp"))
    image_utils.createThumbnail(imageFilePath)

    if fileType == ".png":
        image_utils.limitSize(imageFilePath)

    return True


def deleteImage(location):
    try:
        shutil.rmtree(location) #need to get rid of "../"
    except OSError:
        print "Deleting image with no path"

def createGallery(year, galleryName):
    galleryPath = os.path.join(uploadPath, str(year), galleryName)
    if not os.path.exists(galleryPath):
        os.makedirs(galleryPath)
        uploadPath = os.path.join(flaskPath, "uploads")

def deleteGallery(year, galleryName):
    shutil.rmtree(os.path.join(upload_path, year, gallery))

def setupDB():
    os.makedirs(upload_path)

def reloadDB():
    if os.path.exists(upload_path):
        shutil.rmtree(upload_path)
        setupDB()

