#Flask CMS

##A full cms, implemented in python

__Templates__
__Blocks__
__Pages__
__Blogs__
__tags__
__Comments__


just put your settings in settings.py

then system and database info in the local\_settings.py file

for a quick db setup just add <code>SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'</code>

to local\_settings.py and the in the shell type


<kbd>python manage.py db upgrade</kbd>

after a few seconds:



<kbd>./start.sh</kbd>

then you should see:

```shell
 * Running on http://0.0.0.0:8080/
 * Restarting with reloader
```

then just connect to your ip address: ie
192.168.1.155:8080 or 127.0.0.1:8080
or w/e yours is 
---


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/jstacoder/flask-cms/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

