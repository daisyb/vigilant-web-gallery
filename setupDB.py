import utils2
utils2.run_sql("DROP TABLE IF EXISTS images")
utils2.setup_db()
utils2.add_gallery(2016, "line")
utils2.add_gallery(2016, "final")
utils2.add_gallery(2015, "polygon")
utils2.add_gallery(2014, "edge")
utils2.add_gallery(2013, "3d")
utils2.add_gallery(2012, "mdl")
