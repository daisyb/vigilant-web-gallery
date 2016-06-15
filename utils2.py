import sqlite3
import json
from datetime import date
#import PythonMagick
import os, shutil

flask_path = os.path.dirname(__file__) 
database_path = os.path.join(flask_path, "imagegallery2.db")
upload_path = os.path.join(flask_path, "static/uploads")
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



    con = sqlite3.connect(database_path)
    cur = con.cursor()
    out = cur.execute(sql).fetchall()
    con.close()
    return out

def insert(sql):
    print "database path:" + database_path
    print "flask path:" + flask_path
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
    run_sql("DROP TABLE IF EXISTS images")
    setup_db()




def gallery_exists (year, gallery):
    check_existence = "SELECT CASE WHEN EXISTS ( SELECT * FROM images WHERE gallery = '" + gallery + "' AND year = "+ str(year) + " ) THEN CAST(1 AS BIT) ELSE CAST (0 AS BIT) END;"
    return run_sql(check_existence)[0][0]

def image_exists (year, gallery, name):
    check_existence = "SELECT CASE WHEN EXISTS ( SELECT * FROM images WHERE gallery = '" + gallery + "' AND year = "+ str(year) + " AND name = '" + name + "' ) THEN CAST(1 AS BIT) ELSE CAST (0 AS BIT) END;"
    return run_sql(check_existence)[0][0]


def show_table():
    print run_sql("SELECT * FROM images")


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
    sql = "SELECT name FROM images WHERE gallery = '" + gallery + "' AND year =" + str(year) + " AND NOT name = ''"
    return run_sql(sql)

def get_current_galleries():
    galleries_query = "SELECT gallery FROM images WHERE name = '' AND archived = 0 AND visible = 1 AND year = " + str(current_year)
    return screw_tuples2(run_sql(galleries_query))

def get_all_galleries():
    galleries_query = "SELECT gallery, year FROM images WHERE name = ''"
    return screw_tuples(run_sql(galleries_query))

def get_galleries_in_year(year):
    galleries_query = "SELECT gallery FROM images WHERE year = " + str(year) + " AND name = ''"
    return screw_tuples2(run_sql(galleries_query))


def add_gallery(year, gallery):
    if gallery_exists(year, gallery):
        return False
    else:
        gallery_path = os.path.join(upload_path, str(year), gallery)
        sql = "INSERT INTO images VALUES ('', '"+ gallery + "', " + str(year) + ", '"+ "', '.png', 0, 0)"
        insert(sql)
        os.makedirs(gallery_path)
        return True


def add_image(year, gallery, name, filetype, image_path):
    # Folder name is different from name cause it has timestamp added
    if image_exists(year, gallery, name):
        return False
    sql = "INSERT INTO images VALUES ('" + name + "', '" + gallery + "', " + str(year) + ", '" + image_path + "', '" + filetype + "', 1, 0)"
    insert(sql)
    return True


def get_sample_images():  #gets one image from each gallery
    current_year = date.today().year
    galleries = get_current_galleries()
    out = []
    for gallery in galleries:
        sql = "SELECT location FROM images WHERE gallery = '" + gallery + "' AND year = " + str(current_year) +  " AND NOT name = '' ORDER BY RANDOM() LIMIT 1"
        dict = {}
        dict["gallery"] = gallery
        sql_out = run_sql(sql)
        print sql_out
        try:
            dict["path"] = sql_out[0][0]
        except IndexError:
            dict["path"] = "static/images"
        out.append(dict)
    return out
    
def set_visible_by_year(year, visible):
    sql = "UPDATE images SET visible = " + visible + "WHERE year = " + year 
    insert(sql)

def get_visible_by_year(year):
    visible_query = "SELECT gallery FROM images WHERE year = " + year " AND visible = 1"
    return screw_tuples2(run_sql(visible_query))

def get_invisible_by_year(year):
    visible_query = "SELECT gallery FROM images WHERE year = " + year " AND visible = 0"
    return screw_tuples2(run_sql(visible_query))

def delete_image(year, gallery, name):
    if image_exists(year, gallery, name):
        location_query = "SELECT location FROM images WHERE name = '" + name + "' AND gallery = '" + gallery + "' AND year = " + str(year)
        location = run_sql(location_query)[0][0]
        print location
        delete_query= "DELETE FROM images WHERE year = " + str(year) + " AND gallery = '" + gallery + "' AND name = '" + name + "'"
        print delete_query
        insert(delete_query)
        try:
            shutil.rmtree(location)
        except OSError:
            print "Deleting image with no path"
        return True
    return False

def delete_gallery(year, gallery):
    if gallery_exists(year, gallery):
        delete = "DELETE FROM image WHERE gallery = '" + gallery + "' AND year = " + year
        insert(delete)
        shutil.rmtree(os.path.join(upload_path, year, gallery))
        return True
    return False

def set_archive(year, archive):
    sql = "UPDATE image SET archive = " + str(archive) + "WHERE year = " + year
    insert(sql)

def get_galleries_by_archived(archived):
    sql = "SELECT DISTINCT gallery, year FROM images WHERE archived = " + archived
    sql_out = run_sql(sql)
    out = []
    for gallery in sql_out:
        dict = {}
        dict['gallery'] = gallery[0]
        dict['year'] = gallery[1]
        out.append(dict)
    return out


def get_archived_galleries():
    return get_galleries_by_archived(1)

def get_unarchived_galleries():
    return get_galleries_by_archived(0)
        


def get_images(gallery):
    path_query = "SELECT name, location, filetype FROM images WHERE gallery = '" + gallery + "' AND NOT name = '' "
    sql_out = run_sql(path_query)
    out = []
    for i in sql_out:
        dict = {}
        dict['title'] = i[0]
        dict['path'] = i[1]
        dict['filetype'] = i[2]
        out.append(dict)
    return  out
    

def get_images_in_gallery(year, gallery):
    image_query = "SELECT name FROM images WHERE gallery = '" + gallery + "' "
    return screw_tuples2(run_sql(image_query))

def get_years():
    years_query = "SELECT DISTINCT year FROM images WHERE name = '' "
    return screw_tuples2(run_sql(years_query))

def get_previous_years():
    return get_years().remove(current_year)
