import sqlite3

con = sqlite3.connect("imagegallery.db")

cur = con.cursor()

sql = "CREATE TABLE IF NOT EXISTS images(title TEXT, imagepath TEXT, thumbnailpath TEXT, githublink TEXT)"
cur.execute(sql)

con.commit()
con.close()
