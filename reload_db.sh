cd /var/www/vigilantwebgallery/vigilantwebgallery/static
rm -rf uploads
cd ..
python setupDB.py
cd ..
chown -R www-data:www-data vigilantwebgallery
service apache2 restart
service apache2 reload
