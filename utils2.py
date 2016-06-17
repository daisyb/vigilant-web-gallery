import sqlite3
import json
from datetime import date
import PythonMagick
import os, shutil

flask_path = os.path.dirname(__file__) 
database_path = os.path.join(flask_path, "imagegallery2.db")
upload_path = os.path.join(flask_path, "static/uploads")


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

def run_sql_params(sql, *args):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    out = cur.execute(sql, args).fetchall()
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

def insert_params(sql, *args):
    print "database path:" + database_path
    print "flask path:" + flask_path
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.execute(sql, args)
    con.commit()
    con.close()
    
def setup_db():
    setup_table = "CREATE TABLE IF NOT EXISTS images (name TEXT, gallery TEXT, year INTEGER, location TEXT, filetype TEXT, visible INTEGER, archived INTEGER )"
    run_sql(setup_table)
    if os.path.exists(upload_path):
        shutil.rmtree(upload_path)
    os.makedirs(upload_path)
    
def reload_db():
    run_sql("DROP TABLE IF EXISTS images")
    setup_db()


def gallery_exists (year, gallery):
    #check_existence = "SELECT CASE WHEN EXISTS ( SELECT * FROM images WHERE gallery = '" + gallery + "' AND year = "+ str(year) + " ) THEN CAST(1 AS BIT) ELSE CAST (0 AS BIT) END;"
    #return run_sql(check_existence)[0][0]
    check_existence = "SELECT CASE WHEN EXISTS ( SELECT * FROM images WHERE gallery = ? AND year = ? ) THEN CAST(1 AS BIT) ELSE CAST (0 AS BIT) END;"
    return run_sql_params(check_existence, gallery, str(year))[0][0]

def image_exists (year, gallery, name):
    #check_existence = "SELECT CASE WHEN EXISTS ( SELECT * FROM images WHERE gallery = '" + gallery + "' AND year = "+ str(year) + " AND name = '" + name + "' ) THEN CAST(1 AS BIT) ELSE CAST (0 AS BIT) END;"
    #return run_sql(check_existence)[0][0]
    check_existence = "SELECT CASE WHEN EXISTS ( SELECT * FROM images WHERE gallery = ? AND year = ? AND name = ? ) THEN CAST(1 AS BIT) ELSE CAST (0 AS BIT) END;"
    return run_sql_params(check_existence, gallery, str(year), name)[0][0]
    


def show_table():
    print run_sql("SELECT * FROM images")

# <---------------------- Image Tools ---------------------->

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


def create_thumbnail(imagepath):   #creates a thumbnail named "thumbnail.png"
    image = PythonMagick.Image(str(imagepath))
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

    newpath = str(imagepath)[:-9]
    newpath += "thumbnail.png"
    image.write(newpath)
    return True

def limit_size(imagepath):
    print imagepath 
    image = PythonMagick.Image(str(imagepath))
    geometry = image.size()
    w, h = float(geometry.width()), float(geometry.height())

    new_size = 1000
    if (w > new_size or h > new_size):
        if (w > h):
            image = resize(image, 1000, int(1000 * (h/w)))
        else:
            image = resize(image, int(1000 * (w/h)), 1000)
        image.write(str(imagepath))
    return True

# <---------------------- Images  ---------------------->

def get_images_in_gallery(year, gallery):
    #sql = "SELECT name, location, filetype FROM images WHERE gallery = '" + gallery + "' AND year =" + str(year) + " AND NOT name = '' AND visible = 1"
    #sql_out = run_sql(sql)
    sql = "SELECT name, location, filetype FROM images WHERE gallery = ? AND year = ? AND NOT name = '' AND visible = 1"
    sql_out = run_sql_params(sql, gallery, str(year))
    out = []
    for i in sql_out:
        dict = {}
        dict['title'] = i[0]
        dict['path'] = i[1]
        dict['filetype'] = i[2]
        out.append(dict)
    return out


def get_images(gallery):
    return get_images_in_gallery(date.today().year, gallery)

def add_image(year, gallery, name, filetype, image_path):
    # Folder name is different from name cause it has timestamp added
    if image_exists(year, gallery, name):
        return False
    #sql = "INSERT INTO images VALUES ('" + name + "', '" + gallery + "', " + str(year) + ", '" + image_path + "', '" + filetype + "', 1, 0)"
    #insert(sql)

    sql = "INSERT INTO images VALUES (?, ?, ?, ?, ?, 1, 0)"
    insert_params(sql, name, gallery, str(year), image_path, filetype)
    return True

def get_sample_images():  #gets one image from each gallery
   
    galleries = get_current_galleries()
    out = []
    for gallery in galleries:
        #sql = "SELECT location FROM images WHERE gallery = '" + gallery + "' AND year = " + str(date.today().year) +  " AND NOT name = '' ORDER BY RANDOM() LIMIT 1"
        sql = "SELECT location FROM images WHERE gallery = ? AND year = " + str(date.today().year) +  " AND NOT name = '' ORDER BY RANDOM() LIMIT 1"
        dict = {}
        dict["gallery"] = gallery
        #sql_out = run_sql(sql)
        sql_out = run_sql_params(sql, gallery)
        print sql_out
        try:
            dict["path"] = sql_out[0][0]
        except IndexError:
            dict["path"] = "static/images"
        out.append(dict)
    return out

def delete_image(year, gallery, name):
    if image_exists(year, gallery, name):
        #location_query = "SELECT location FROM images WHERE name = '" + name + "' AND gallery = '" + gallery + "' AND year = " + str(year)
        #location = run_sql(location_query)[0][0]
        location_query = "SELECT location FROM images WHERE name = ? AND gallery = ? AND year = ?"
        location = run_sql_params(location_query, name, gallery, str(year))[0][0]
        print location[3:]
        
        #delete_query= "DELETE FROM images WHERE year = " + str(year) + " AND gallery = '" + gallery + "' AND name = '" + name + "'"
        delete_query= "DELETE FROM images WHERE year = ? AND gallery = ? AND name = ?"
        print delete_query
        #insert(delete_query)
        insert_params(delete_query, str(year), gallery, name)
        try:
            shutil.rmtree(location[3:]) #need to get rid of "../"
        except OSError:
            print "Deleting image with no path"
        return True
    return False


# <---------------------- Galleries  ---------------------->

def get_current_galleries():
    galleries_query = "SELECT gallery FROM images WHERE name = '' AND archived = 0 AND visible = 1 AND year = " + str(date.today().year)
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
        sql = "INSERT INTO images VALUES ('', '"+ gallery + "', " + str(year) + ", '"+ "', '.png', 1, 0)"
        insert(sql)
        os.makedirs(gallery_path)
        return True


def set_visible(year, gallery, visible):
     sql = "UPDATE images SET visible = " + str(visible) + " WHERE gallery = '" + gallery +  "' AND year = " + str(year)
     insert(sql)


def set_visible_by_year(year, visible):
    sql = "UPDATE images SET visible = " + str(visible) + " WHERE year = " + str(year) 
    insert(sql)

def get_visible_by_year(year):
    visible_query = "SELECT gallery FROM images WHERE year = " + str(year) + " AND visible = 1"
    return screw_tuples2(run_sql(visible_query))

def get_invisible_by_year(year):
    visible_query = "SELECT gallery FROM images WHERE year = " + str(year) + " AND visible = 0"
    return screw_tuples2(run_sql(visible_query))

def get_invisible_by_year(year):
    visible_query = "SELECT gallery FROM images WHERE year = " + year + " AND visible = 0"
    return screw_tuples2(run_sql(visible_query))


def delete_gallery(year, gallery):
    if gallery_exists(year, gallery):
        delete = "DELETE FROM images WHERE gallery = '" + gallery + "' AND year = " + year
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
        


def get_years():
    years_query = "SELECT DISTINCT year FROM images WHERE name = '' "
    return screw_tuples2(run_sql(years_query))

def get_previous_years():
    years = get_years()
    years.remove(date.today().year)
    return years

def get_invisible_years():
    years_query = "SELECT DISTINCT year FROM images WHERE visible = 0"
    return screw_tuples2(run_sql(years_query))

def get_visible_years():
    years_query = "SELECT DISTINCT year FROM images WHERE visible = 1"
    return screw_tuples2(run_sql(years_query))
