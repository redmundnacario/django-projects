# Create your First Django API

## Contents:
* Requirements
* Installation
* Create your First  Django Project
* Create your First Django Application
* Create your First Django API

## Requirements
* Python 3
* bash terminal
* Microsoft Visual Studio Code (VSCode)

## Installation
```bash
pip install django
pip install pillow
```


## Create your First Project

1.  Create a new project
 
```bash
django-admin startproject <name-of-project>
```

2. Migrate, create user and password.


```bash
cd <name-of-project>
python manage.py migrate
python manage.py createsuperuser
```

3. Openthe VS done and set up debugging options VSCODE

```bash
code .
```

* edit the launch.json. Set “program” to file path of manage.py
* comment “—nothreading””

4. Run the server in the debugging tools


## Create your First Application

1. Start an app.

```bash
python manage.py startapp <name-of-application>
```
	
2. Series of steps.

	* Set up project settings.py : add <name-of-application> to the "INSTALLED_APPS" list.
	* Set up application model : Classes of table and columns.
	* Set up application views: Classes of views per model.
	* Set up application template : html file.
	* Set up application urls.py : List of urlpatterns per views.
	* Set up project urls.py : List of urlpatterns from apps.
	* Set up project settings.py : set up variables for Media : MEDIA_ROOT, MEDIA_URL (optional).
	* Set up application admin.py : Register views in admin site.

3. Run Make migrations - Do this every edit in models

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Run server
	* run code in debug options of VScode
	* result will be a blank page, need to create sample inputs in the admin page.


## Create your First API

0. Set up project views : Create functions that return json response
1. Set up project urls : List of urls per view functions
2. Set up application urls: edit url (i.e “api/“)

