# In-House
COS397 Project Repository for In-House Operations

Instructions on running local server:

## Requirements
Packages can be installed using pip or your preferred package manager:   
```Django```  
```psycopg2```  
```django-extensions```  
```djangorestframework```  
```gunicorn```

## Get Postgresql installed locally
https://www.postgresql.org/download/

### Important Information about your local database
1. open PGadmin
2. create a new database with:
    - *name:* csbldb
    - *username:* pgadmin
    - *password:* orange

This is important because the manage.py file points to this database!


### To run the server and see the site:

enter the following shell command in the `in-house/inhouse` folder

``` shell
$ python manage.py runserver

```

then open browser and navigate to:
### http://127.0.0.1:8000/boardmanlab/


Helpful database query (to destroy all):
``` shell
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```
