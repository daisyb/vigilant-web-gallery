import urllib2, json
key = "nyang"
functions = ["Delete Image", "Delete Gallery", "Add Gallery", "Get Galleries", "Archive Year", "List Years"]
def main():
    print "Welcome Mr. DW!"
    print "What do you want to do?"
    printFunctions() # function that prints available functions
    goal = raw_input()

    if goal == 0:
        deleteImage()


def printFunctions():
    printList(functions)

def callAPI(url):
    print url
    request = urllib2.urlopen(url)
    result = request.read()
    return  json.loads(result)

def getImages(gallery):
    uri = "http://107.170.107.124:8001/getimagename/%s/%s"
    url = uri%(key, gallery)
    return callAPI(url)

def getGalleries():
    uri = "http://107.170.107.124:8001/getgalleries/%s"
    url = uri%(key)
    return callAPI(url)

def printList(coll):
    for index, item in coll:
        print str(index) + " " + gallery

def askGallery():
    print "Here are the galleries:"
    galleries = getGalleries()
    printList(galleries)
    galleryNum = raw_input("Please select the number of the gallery you would like:")
    if int(galleryNum) > len(galleries) or int(galleryNum) < 0:
        print "Please give a valid number"
        return askGallery()
    return galleryNum


def deleteImage():
    galleryNum = askGallery()
    print "Here are the images in " + galleries[galleryNum]
    images = getImages(gallery)
    printList(getImages)
    imageNum = raw_input("Please select the number of the image you would like:")
    confirm = raw_input("You want to delete " + images[imageNum] + "in" + galleries[galleryNum] + "(y/n)")
    if confirm.lower == "y":
        uri = "http://107.170.107.124/deleteimage/%s/%s/%s"
        url = uri%(key, images[imageNum], galleries[galleryNum])
        print callApi(url)

def deleteGallery():
    galleryNum = askGallery()
    
    
