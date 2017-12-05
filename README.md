# Database
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=areaparking -d mysql:5.7.20 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

# MAC OSの場合：下記のエラーが発生した場合
django.contrib.gis.geos.error.GEOSException: Could not parse version info string "3.6.2-CAPI-1.10.2 4d2925d6"
解決方法は以下になります：
https://stackoverflow.com/questions/18643998/geodjango-geosexception-error
