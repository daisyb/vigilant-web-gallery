import sqlite3

con = sqlite3.connect("imagegallery.db")

cur = con.cursor()

sql = "CREATE TABLE IF NOT EXISTS images(title TEXT, imagepath TEXT, thumbnailpath TEXT, codepath TEXT)"
cur.execute(sql)
sql = "CREATE TABLE IF NOT EXISTS allGalleries(year integer, galleryname TEXT, visible integer)"  #0 for false, 1 for true
cur.execute(sql)
con.commit()
con.close()
