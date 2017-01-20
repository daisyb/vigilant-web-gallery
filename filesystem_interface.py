import os
from werkzeug.utils import secure_filename

flaskPath = os.path.dirname(__file__)
uploadPath = os.path.join(flaskPath, "uploads")

try:
    os.symlink(uploadPath, os.path.join(flaskPath, "static", "uploads"))
except OSError:
    print "Already symlinked"

def validGIF(tempSize):
    return tempSize > 10 * 1024 * 1024

def validPNG(tempSize):
    return tempSize > 5 * 1024 * 1024

def validFile(tempSize, fileType):
    if fileType == ".gif" and not validGIF(tempPath):
        return """Your file is too large. The maximum allowed file
                  size for a .gif is 10 megabytes."""

    if fileType == ".png" and not validPNG(tempPath):
        return """Your file is too large. The maximum allowed file
                  size for a .png is 5 megabytes."""
    return True

def createImage(imageName, year, galleryName, fileType):
    tempName = str(uuid.uuid4())
    tempPath = os.path.join(flaskPath, 'temp', tempName)
    file.save(tempPath) #file is saved as temp
    tempSize = os.path.getsize(tempPath)
    fileValid = validFile(tempSize, fileType)
    if fileValid != True:
        return fileValid

    folderName = secure_filename(imageName + "_" + str(int(time.time())))
      #sets foldername to first_last_timestamp
    relativeImageDir = os.path.join("Uploads",
                                      str(year),
                                      galleryName,
                                      folderName)
    imageDir = os.path.join(flaskPath, relativeImageDir)
    os.makedirs(imageDir)
    imageFilePath = os.path.join(image_dir,
                                 "image" + fileType)
    os.rename(tempPath, imageFilePath)
    f = open(image_dir + "/code.txt", 'w')
    f.write(code)
    f.close()
    shutil.rmtree(os.path.join(flaskPath, "temp"))
    os.makedirs(os.path.join(flaskPath, "temp"))
    return True


def deleteImage(location):
    try:
        shutil.rmtree(location[3:]) #need to get rid of "../"
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

