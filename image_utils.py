try:
    import PythonMagick
except ImportError:
    print "PythonMagick not installed"
import os

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


def createThumbnail(imageDir, fileType):   #creates a thumbnail named "thumbnail.png"
    imageFile = os.path.join(imageDir, "image" + fileType)
    image = PythonMagick.Image(str(imageFile))
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

    newPath = os.path.join(imageDir, "thumbnail.png")
    image.write(str(newPath))
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
