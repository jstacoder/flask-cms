# Flask CMS

## A full cms, implemented in python, built on top of [Flask-XXL](https://github.com/jstacoder/flask-xxl)

for documentation on layout, concepts etc.. see the [Flask-XXL wiki](https://github.com/jstacoder/flask-xxl/wiki)

__Templates__  
__Blocks__  
__Pages__  
__Blogs__  
__tags__  
__Comments__  


to try it out just use docker-compose:
  - first checkout the repo
    - `git clone https://github.com/jstacoder/flask-cms.git && cd flask-cms`
  - then build the app using docker compose
    - `docker-compose build`
  - then if this is the first time you've ran this you need to initalize your database
    - `docker-compose run app /initalize.sh`
  - and now you can go ahead and run the app
    - `docker-compose up`   
  
  after a few seconds you should see:

```bash
 * Running on http://0.0.0.0:5000/
 * Restarting with reloader
```

then just connect to your docker ip address,   
proably just localhost




