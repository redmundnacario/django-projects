# Serializers

## Contents

## 1. Construct your data model in <name-of-application>/models.py.
```python
from django.db import models

# Create your models here.

class Article(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    body = models.TextField()
    location = models.CharField(max_length=120)
    publication_date = models.DateField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{ self.author } { self.title }"
```


## 2. Create "api" folder in your application. In this folder, the following files must be present:
- serializer.py
- urls.py
- views.py

## 3. Create the <name-of-application>/api/serializer.py

```python
from rest_framework import serializers
from news.models import Article

# read_only is true to automatic django input not user input
class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    body = serializers.CharField()
    location = serializers.CharField()
    publication_date = serializers.DateField()
    active = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.author = validated_data.get("author", instance.author)
        instance.title = validated_data.get("title", instance.title)
        instance.body = validated_data.get("body", instance.body)
        instance.description = validated_data.get("description", instance.description)
        instance.body = validated_data.get("body", instance.body)
        instance.location = validated_data.get("location", instance.location)
        instance.publication_date = validated_data.get("publication_date", instance.publication_date)
        instance.active = validated_data.get("active", instance.active)
        instance.save()
        return instance
```

## 4. Create the <name-of-application>/api/views.py

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from news.models import Article
from news.api.serializers import ArticleSerializer

@api_view(["GET", "POST"])
def article_list_create_api_view(request):
    if request.method == "GET":
        articles = Article.objects.filter(active=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(data=serializer.data)
    
    elif request.method == "POST":
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT","DELETE"])
def article_detail_api_view(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response({"error": {
                            "code" : 404,
                            "message" : "Article not found!"
                        }}, status = status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ArticleSerializer(article)
        return Response(data = serializer.data)

    elif request.method == "PUT":
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
```

## 5. Create the <name-of-application>/api/urls.py
```python
from django.urls import path
from news.api.views import article_list_create_api_view,\
                           article_detail_api_view
                        
urlpatterns = [
    path("articles/",article_list_create_api_view,name="article-list"),
    path("articles/<int:pk>",article_detail_api_view, name="article-detail")
]
```

## 6. Do not forget to edit the <name-of-project>/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("news.api.urls"))
]
```
## 7. Run the debugger in VScode