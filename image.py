from werkzeug.utils import secure_filename


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

    fileType = imageFile.filename[-4:].lower(),

    imageValid = validImage(imageName,
                           galleryName,
                           galleries,
                           fileType)
    if imageValid != True:
        return imageValid

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
        location = sqlite_interface.getImageLocation(year,
                                                     galleryName,
                                                     imageName)
        filesystem_interface.deleteImage(location)
        return insertedProperly

    if savedProperly != True:
        sqlite_interface.deleteImage(year, galleryName, imageName)
        return savedProperly

    return True

def delete(year, gallery, name)

