# Setting up Django Rest Framework and Introduction to Serializer

## 1. Setting up Django
1. Create a virtual environment then activate it.

```bash
python3 -m venv <name-of-environment>
source <name-of-environment>/bin/activate
```

2. Upgrade pip.

3. Install Django and Django Rest Framework.

```bash
pip install django djangorestframework
```

4. Create your Django project and open VSCode in the project directory

```bash
django-admin startproject <name-of-project>
cd <name-of-project>
code .
```

5. Select a python interpreter . I must be pointing to the previously created environment. You can also manually put the directory of the environment in settings>workspace>venv.
 
6. Create an application

```bash
python manage.py startapp <name-of-application>
```

7. Make sure to add the apps created and “rest_framework” in an existing list named INSTALLED_APPS in <name-of-project>/settings.py



## 2. Serializer and Deserializer
```bash
cd <name-of-application>
```

1. Create model  classes in the application created in the project: target file is models.py
2. Create “api” folder inside the created application. Create a file named serializers.py. Then create a serializers as python Class
3. Add create and update methods inside the serializer.
4. Run app and add sample data in admin site
5. Test the setting in terminal of vscode.
```bash
$ python manage.py shell
Python 3.7.4 (default, Aug 13 2019, 15:17:50) 
[Clang 4.0.1 (tags/RELEASE_401/final)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```

### Serializing

6. Import the models classes and serializers classes. Serialize the created data in admin site. Serialized data are python native data

```python
>>> from news.models import Article
>>> from news.api.serializers import ArticleSerializer
>>> article_instance = Article.objects.first()
>>> article_instance
<Article: John Doe To kill a mocking bird>
>>> serializer = ArticleSerializer(article_instance)
>>> serializer
ArticleSerializer(<Article: John Doe To kill a mocking bird>):
    id = IntegerField(read_only=True)
    author = CharField()
    title = CharField()
    description = CharField()
    body = CharField()
    location = CharField()
    publication_date = DateField()
    active = BooleanField()
    created_at = DateTimeField(read_only=True)
    updated_at = DateTimeField(read_only=True)
>>> serializer.data
{'id': 1, 'author': 'John Doe', 'title': 'To kill a mocking bird', 'description': 'Very long to read.', 'body': 'lorem ipsum dolor', 'location': 'Mandaluyong City', 'publication_date': '2020-03-01', 'active': True, 'created_at': '2020-04-08T20:13:07.193598Z', 'updated_at': '2020-04-08T20:13:07.193666Z'}
```

7. Import JSONRenderer from rest_framework and convert the serialized data.

```python
>>> from rest_framework.renderers import JSONRenderer
>>> json = JSONRenderer().render(serializer.data)
>>> json
b'{"id":1,"author":"John Doe","title":"To kill a mocking bird","description":"Very long to read.","body":"lorem ipsum dolor","location":"Mandaluyong City","publication_date":"2020-03-01","active":true,"created_at":"2020-04-08T20:13:07.193598Z","updated_at":"2020-04-08T20:13:07.193666Z"}'
```

### Deserializing
- - - -

8. Import IO and JSONParser . Convert the previous JSON data by IO and JSONParser back to python native data. This process is Deserialization

```python
>>> import io
>>> from rest_framework.parsers import JSONParser
>>> stream = io.BytesIO(json)
>>> stream
<_io.BytesIO object at 0x104f5d2f0>
>>> data = JSONParser().parse(stream)
>>> data
{'id': 1, 'author': 'John Doe', 'title': 'To kill a mocking bird', 'description': 'Very long to read.', 'body': 'lorem ipsum dolor', 'location': 'Mandaluyong City', 'publication_date': '2020-03-01', 'active': True, 'created_at': '2020-04-08T20:13:07.193598Z', 'updated_at': '2020-04-08T20:13:07.193666Z'}
```

9. Then we restore those native datatypes into a dictionary of validated data.

```python
>>> serializer = ArticleSerializer(data =data)
>>> serializer.is_valid()
True
>>> serializer.validated_data
OrderedDict([('author', 'John Doe'), ('title', 'To kill a mocking bird'), ('description', 'Very long to read.'), ('body', 'lorem ipsum dolor'), ('location', 'Mandaluyong City'), ('publication_date', datetime.date(2020, 3, 1)), ('active', True)])
```

10. Save the data as another instance.

```python
>>> serializer.save()
<Article: John Doe To kill a mocking bird>
```

11. Notice that there are two instances in the objects.

```python
>>> Article.objects.all()
<QuerySet [<Article: John Doe To kill a mocking bird>, <Article: John Doe To kill a mocking bird>]>
>>> 
```
