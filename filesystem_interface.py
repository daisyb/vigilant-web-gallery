import os
from werkzeug.utils import secure_filename

flaskPath = os.path.dirname(__file__)
uploadPath = os.path.join(flaskPath, "uploads")

try:
    os.symlink(uploadPath, os.path.join(flaskPath, "static", "uploads"))
except OSError:
    print "Already symlinked"

def createImage(imageName, year, galleryName):
    tempName = str(uuid.uuid4())
    tempPath = os.path.join(flaskPath, 'temp', tempName)
    file.save(tempPath) #file is saved as temp
    folderName = secure_filename(imageName + "_" + str(int(time.time())))
      #sets foldername to first_last_timestamp
    relativeImageDir = os.path.join("Uploads",
                                      str(year),
                                      galleryName,
                                      folderName)
    imageDir = os.path.join(flaskPath, relativeImageDir)
    os.makedirs(imageDir)
    imageFilePath = os.path.join(image_dir,
                                 "image" + filetype)
    os.rename(temppath, image_file_path)
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

