import os
import utils2
import time
from werkzeug.utils import secure_filename

flask_path = os.path.dirname(__file__) 
print "What YEAR are you adding images to?"
year = raw_input()
print "What gallery in that year are you adding to?"
gallery = raw_input()
static_path = "static/uploads/" + str(year) + "/" + gallery
print
print "Before we continue please make sure that all the images you wish to add are in this path:"
print static_path + "/"
print "Coninue? y/n"
cont = raw_input()
if cont.lower() != 'y' and cont.lower() != 'yes':
    exit()

utils2.add_gallery(year, gallery)
dir_contents =  os.listdir(static_path)
print "During this process submission names are automatically stored"
print "in the gallery as the name of the image file"
print "For example, goat.jpg will have the submission title 'goat'"
print "Would you like to manually input submission tiles instead?(y/n)"
yorn = raw_input()
manual = True
if yorn.lower() != 'y' and yorn.lower() != 'yes':
    manual = False
for img in dir_contents:
    if img.lower().endswith('.png') or img.lower().endswith('.gif'):
        if manual:
            print "Submission title for: " + img
            name = raw_input()
        else:
            name = img[:-4]
        extension = img[-4:].lower()
        
        file = img
        gallname = gallery
        image_name = name
        temppath = os.path.join(flask_path, static_path, img)
        foldername = secure_filename(image_name + "_" + str(int(time.time()))) #sets foldername to first_last_timestamp
        current_year = year
        relative_image_dir = os.path.join(static_path, foldername)

        if utils2.add_image(current_year, gallname, image_name,
                            extension, "../" + relative_image_dir):
            image_dir = os.path.join(flask_path, relative_image_dir)
            os.makedirs(image_dir)
            image_file_path = image_dir + "/image" + extension
            os.rename(temppath, image_file_path)
            print image_file_path
            utils2.create_thumbnail(image_file_path)
            f = open(image_dir + "/code.txt", 'w')
            #f.write(code)
            f.close()
Status API Training Shop Blog About
