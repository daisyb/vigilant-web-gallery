import sqlite3
import json
from datetime import date
import PythonMagick
import os, shutil

flask_path = os.path.dirname(__file__) + "/"
database_path = flask_path + "imagegallery2.db"
upload_path = flask_path + "static/uploads/"
current_year = date.today().year
'''
Take 2

Basically here's the setup:
One huge table:
| name        |  gallery    | year    |   location           | filetype |  visible     | archived     |
|-------------|-------------|---------|----------------------|----------|--------------|--------------|
| text        | text        | int     |  text                | text     | int (0 or 1) | int (0 or 1) |
| bob's image | line        | 2016    | /2016/line/bobsimage | .png     | 1            |  1           |

'''

# <---------------------- Utils ---------------------->
def screw_tuples(shitty_tuple_list):
    return  [str(i[1]) + i[0] for i in shitty_tuple_list]

def screw_tuples2(shitty_tuple_list):
    return [i[0] for i in shitty_tuple_list]

def run_sql(sql):
    print "flask path:" + flask_path
    print "database path:" + database_path
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    return  cur.execute(sql)

def insert(sql):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def setup_db():
    setup_table = "CREATE TABLE IF NOT EXISTS images (name TEXT, gallery TEXT, year INTEGER, location TEXT, filetype TEXT, visible INTEGER, archived INTEGER )"
    run_sql(setup_table)
    os.makedirs(upload_path)
def reload_db():
    run_sql("DROP TABLE images")
    shutil.rmtree(upload_path)
    setup_db()


def gallery_exists (year, gallery):
    check_existence = "SELECT CASE WHEN EXISTS ( SELECT * FROM images WHERE gallery = '" + gallery + "' AND year = "+ str(year) + " ) THEN CAST(1 AS BIT) ELSE CAST (0 AS BIT) END;"
    return run_sql(check_existence).fetchall()[0][0]

def image_exists (year, gallery, name):
    check_existence = "SELECT CASE WHEN EXISTS ( SELECT * FROM images WHERE gallery = '" + gallery + "' AND year = "+ str(year) + " AND name = '" + name + "' ) THEN CAST(1 AS BIT) ELSE CAST (0 AS BIT) END;"
    return run_sql(check_existence).fetchall()[0][0]


def show_table():
    print run_sql("SELECT * FROM images").fetchall()


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


def create_thumbnail(imagepath):   #just returns True for now. creates a thumbnail named "thumbnail.png"
    image = PythonMagick.Image(str(imagepath))
    #image = image.write("thumbnail.png")
    geometry = image.size()
    w, h = geometry.width(), geometry.height()
    if (w > h):
        center = w/2
        image = crop(image, int(center - h/2), 0, h, h)
        #image.crop(int((center - h/2)),  #left
        #           0,               #top
        #           int((center + h/2)),  #right
        #           int(h))               #bottom
    else:
        center = h/2
        image = crop(image, 0, int(center - w/2), w, w)
        #image.crop(0,                            #left
        #           int((center - w/2)),               #top
        #           int(w),                            #right
        #           int((center + w/2)))               #bottomimage.crop()

    new_size = 175
    image = resize(image, new_size, new_size)
    #image.resize("{}x{}".format(new_size, new_size))
    #image.resize(new_size, new_size)
    newpath = str(imagepath)[:-9]
    newpath += "thumbnail.png"
    image.write(newpath)
    return True

def limit_size(imagepath):
    print imagepath 
    image = PythonMagick.Image(str(imagepath))
    geometry = image.size()
    w, h = geometry.width(), geometry.height()

    new_size = 1000
    if (w > new_size or h > new_size):
        image = resize(image, new_size, new_size)
        #image.resize("{}x{}".format(new_size, new_size))
        #image.resize(new_size, new_size)
        image.write(str(imagepath))
    return True

def get_images_in_gallery(year, gallery):
    sql = "SELECT name FROM images WHERE gallery = '" + gallery + "' AND year ='" + str(year) + "'"
    return run_sql(sql).fetchall()

def get_current_galleries():
    galleries_query = "SELECT gallery FROM images WHERE name = '' AND year = " + str(current_year)
    return screw_tuples2(run_sql(galleries_query).fetchall())

def get_all_galleries():
    galleries_query = "SELECT gallery, year FROM images WHERE name = ''"
    return screw_tuples(run_sql(galleries_query).fetchall())

def add_gallery(year, gallery):
    if gallery_exists(year, gallery):
        return False
    else:
        gallery_path =  upload_path +  "/" + str(year) +  "/"  + gallery
        sql = "INSERT INTO images VALUES ('', '"+ gallery + "', " + str(year) + ", '"+ "', '.png', 0, 0)"
        insert(sql)
        os.makedirs(gallery_path)


def add_image(year, gallery, name, filetype, image_path):
    # Folder name is different from name cause it has timestamp added
    if image_exists(year, gallery, name):
        return False
    sql = "INSERT INTO images VALUES ('" + name + "', '" + gallery + "', " + str(year) + ", '" + image_path + "', '" + filetype + "', 1, 0)"
    print sql
    insert(sql)
    return True


def get_sample_images():  #gets one image from each gallery
    current_year = date.today().year
    galleries = get_current_galleries()
    out = {}
    for gallery in galleries:
        sql = "SELECT location FROM images WHERE gallery = " + gallery + "AND year = " + str(current_year) +  " AND NOT name = '' ORDER BY RANDOM() LIMIT 1"
        if run_sql(sql) == None:
            out[gallery] = "images/thluffy-big.png"
        else:
            out[gallery] = run_sql(sql) + "image.png"
    return out
    
def set_visible(year, visible):
    sql = "UPDATE images SET visible = " + visible + "WHERE year = " + year
    insert(sql)

def get_visible_galleries():
    sql = "SELECT gallery, year FROM images WHERE visible = 1"
    return screw_tuples(run_sql(sql).fetchall())

def get_invisible_galleries():
    sql = "SELECT gallery, year FROM images WHERE visible = 0"
    return screw_tuples(run_sql(sql).fetchall())

def delete_image(year, gallery, name):
    if image_exists(year, gallery, name):
        location_query = "SELECT location FROM images WHERE name = '" + name + "' AND gallery = '" + gallery + "' AND year = " + str(year)
        location = run_sql(location_query).fetchall()[0][0]
        print location
        delete_query= "DELETE FROM images WHERE name = '" + name + "' AND gallery = '" + gallery + "' AND year = " + str(year)
        run_sql(delete_query)
        shutil.rmtree(location)
        return True
    return False

def set_archive(year, archive):
    sql = "UPDATE image SET archive = " + str(archive) + "WHERE year = " + year
    insert(sql)

def get_galleries_by_archived(archived):
    sql = "SELECT gallery, year FROM images WHERE archived = " + archived
    return screw_tuples(run_sql(sql).fetchall())

def get_archived_galleries():
    return get_galleries_by_archived(1)

def get_unarchived_galleries():
    return get_galleries_by_archived(0)
        


def get_image_paths(gallery):
    path_query = "SELECT location FROM images WHERE gallery = '" + gallery + "' AND NOT name = '' "
    return screw_tuples2(run_sql(path_query).fetchall())

def get_images_in_gallery(year, gallery):
    image_query = "SELECT name FROM images WHERE gallery = '" + gallery + "' "
    return screw_tuples2(run_sql(image_query).fetchall())

