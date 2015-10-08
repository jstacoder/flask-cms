#Flask CMS

##A full cms, implemented in python, built on top of [Flask-XXL](https://github.com/jstacoder/flask-xxl)

for documentation on layout, concepts etc.. see the [Flask-XXL wiki](https://github.com/jstacoder/flask-xxl/wiki)

__Templates__  
__Blocks__  
__Pages__  
__Blogs__  
__tags__  
__Comments__  


to use:
  - just put your settings in settings.py
  - then system and database info in the local\_settings.py file

for a quick db setup just add 

```python
class LocalConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///tmp.db"
    SECRET_KEY = "your key"

```

to local\_settings.py (you have to create this file as well) and the in the shell type


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




