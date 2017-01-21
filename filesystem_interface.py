import os, uuid, shutil
import image_utils


ALLOWED_EXTENSIONS = set(['png', 'gif'])
flaskPath = os.path.dirname(__file__)
uploadPath = os.path.join(flaskPath, "static", "uploads")

# Remakes temp every time the app starts
# Before temp got filled up with random junk
try:
    os.makedirs(os.path.join(flaskPath, "temp"))
except OSError:
    print "Already created temp"


# <---------------- Validation ---------------->

def validateGIF(tempSize):
    return tempSize < 10 * 1024 * 1024

def validatePNG(tempSize):
    return tempSize < 5 * 1024 * 1024

def validateFile(tempSize, fileType):
    if fileType == ".gif":
        if not validateGIF(tempSize):
            return """Your file is too large. The maximum allowed file
            size for a .gif is 10 megabytes."""
        return True
    elif fileType == ".png":
        if not validatePNG(tempSize):
            return """Your file is too large. The maximum allowed file
                  size for a .png is 5 megabytes."""
        return True
    return "Invalid file type"

# <---------------- Create/Delete ---------------->
# Basically a simplified implementation of a model pattern
# No Object Oriented stuff though
def createImage(imageFile,
                imageName,
                year,
                galleryName,
                fileType,
                relativeImageDir,
                code):

    tempPath = saveTemp(imageFile)
    tempSize = os.path.getsize(tempPath)

    fileValid = validateFile(tempSize, fileType)
    # validateFile returns True if valid file, error message otherwise
    if fileValid != True:
        return fileValid

    # sets foldername to first_last_timestamp
    # Ideally this should be done in filesystem_interface
    # However, you need the location to insert into the database
    # Best practice would be to do all the path stuff in filesystem_interface
    # then return location to model for it to put into database
    # However that requires returning more than one thing in a function,
    # i.e. a tuple or a hash, which I didn't want to bother with
    imageDir = os.path.join(uploadPath, relativeImageDir)
    os.makedirs(imageDir)
    imageFilePath = os.path.join(imageDir,
                                 "image" + fileType)
    os.rename(tempPath, imageFilePath) # Moves file to imageFilePath

    resetTemp()
    saveCode(imageDir, code)

    image_utils.createThumbnail(imageDir, fileType)

    if fileType == ".png":
        image_utils.limitSize(imageFilePath)

    return True

def resetTemp():
    shutil.rmtree(os.path.join(flaskPath, "temp"))
    os.makedirs(os.path.join(flaskPath, "temp"))

def saveCode(imageDir, code):
    f = open(os.path.join(imageDir, "code.txt"), 'w')
    f.write(code)
    f.close()


def saveTemp(imageFile):
    tempName = str(uuid.uuid4())  # random filename
    tempPath = os.path.join(flaskPath, 'temp', tempName)
    imageFile.save(tempPath) #file is saved as temp
    return tempPath

def deleteImage(location):
    try:
        shutil.rmtree(location)
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

