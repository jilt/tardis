# tardis
Dependencies

pip3 install flask flask-sqlalchemy flask-wtf

pip3 install mysqlclient --- for win10: pip install mysqlclient-1.4.2-cp37-cp37m-win_amd64.whl or similar, depends your system and/or python version
pip3 install Flask-Dropbox
pip3 install configParser
Create a file named example.cfg in the root folder of the project, and write the following insidde the file:
[MySqlConnection]
username = your_username
pwd = your_passphrase
url = your_url_connectionstring
