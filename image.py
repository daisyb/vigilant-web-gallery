import PythonMagick
from werkzeug.utils import secure_filename

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

def validImageName(imageName):
    return not imageName or imageName == ' ' or len(imageName) > 100

def validGalleryName(galleryName, galleries):
    return galleryName not in galleries


def validImage(imageName,
               galleryName,
               galleries,
               fileType):
    if not validImageName(imageName):
        imageNameError = """Invalid image name. Names longer than 100 characters
        or left blank will not display properly. Please change it."""
        return imageNameError

    if not validGalleryName(galleryName, galleries):
        return "Stop trying to be clever"

    if not imageFile or not allowed_file(imageFile.filename):
        return "You did not upload a file or your file name is unacceptable."

    return True

def create(image, galleries, imageFile, year):
    galleryName = image['Gallery']
    fileName = secure_filename(image['name'])
    imageName = " ".join(fileName.split("_"))
    code = image['code'].encode('ascii', 'ignore')

    imageValid = validImage(imageName,
                           galleryName,
                           galleries,
                           fileType)
    if imageValid != True:
        return imageValid

    filetype = imageFile.filename[-4:].lower(),
    savedProperly = filesystem_interface.createImage(imageName,
                                                     year,
                                                     galleryName,
                                                     fileType)
    insertedProperly = sqlite_interface.insertImage(year,
                                                    galleryName,
                                                    imageName,
                                                    filetype,
                                                    relativeImageDir)
    if insertedProperly != True:
        return insertedProperly
    if savedProperly != True:
        return savedProperly

    if fileType == ".png":
        limitSize(imageFilePath)

    createThumbnail(imageFilePath)
    return True


