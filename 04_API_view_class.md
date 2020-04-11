# Using API_view class in Serializing data in Django

## 1. Edit the <name-of-application>/api/views.py

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from news.models import Article
from news.api.serializers import ArticleSerializer

class ArticleListCreateAPIView(APIView):
    
    def get(self, request):
        articles = Article.objects.filter(active=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ArticleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ArticleDetailAPIView(APIView):
    def get_object(self, pk):
        article = get_object_or_404(Article, pk=pk)
        return article

    def get(self,request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
```
## 2. Edit the <name-of-application>/api/urls.py

```python
from django.urls import path
from news.api.views import ArticleListCreateAPIView,\
                           ArticleDetailAPIView
# from news.api.views import article_list_create_api_view,\
#                            article_detail_api_view

urlpatterns = [
    path("articles/", 
         ArticleListCreateAPIView.as_view(),
        name="article-list"),
        
    path("articles/<int:pk>", 
         ArticleDetailAPIView.as_view(), 
         name="article-detail")
]              
```

## 3. Set up Validators

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
    
    def validate(self, data):
        if data["title"] == data["description"]:
            raise serializers.ValidationError("Title and Description must not be the same.")
        return data
    
    def validate_title(self, value):
        if len(value)<10:
            raise serializers.ValidationError("Title must not be less than 10 characters.")
        return value

```

## 3. ModelSerializers

```python

from datetime import datetime
from django.utils.timesince import timesince
from rest_framework import serializers
from news.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    time_since_publication = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = ("id",)

    def get_time_since_publication(self, object):
        publication_date = object.publication_date
        now = datetime.now()
        time_delta = timesince(publication_date, now)
        return time_delta

    def validate(self, data):
        if data["title"] == data["description"]:
            raise serializers.ValidationError("Title and Description must not be the same.")
        return data
    
    def validate_title(self, value):
        if len(value)<10:
            raise serializers.ValidationError("Title must not be less than 10 characters.")
        return value
        
```

## 4. Nested Relationship

- In models.py

```python

from django.db import models

# Create your models here.
class Journalist(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    biography = models.TextField(blank=True)

    def __str__(self):
        return f"{ self.first_name } { self.last_name }"

class Article(models.Model):
    author = models.ForeignKey(Journalist,
                               on_delete=models.CASCADE,
                               related_name='articles')
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

- In serializers.py

```python
from datetime import datetime
from django.utils.timesince import timesince
from rest_framework import serializers
from news.models import Article, Journalist

class ArticleSerializer(serializers.ModelSerializer):
    time_since_publication = serializers.SerializerMethodField()
    author = serializers.StringRelatedField() # show the return value instead of foreign key value

    class Meta:
        model = Article
        exclude = ("id",)

    def get_time_since_publication(self, object):
        publication_date = object.publication_date
        now = datetime.now()
        time_delta = timesince(publication_date, now)
        return time_delta

    def validate(self, data):
        if data["title"] == data["description"]:
            raise serializers.ValidationError("Title and Description must not be the same.")
        return data
    
    def validate_title(self, value):
        if len(value)<10:
            raise serializers.ValidationError("Title must not be less than 10 characters.")
        return value


class JournalistSerializer(serializers.ModelSerializer):
    articles = serializers.HyperlinkedRelatedField(many=True,
                                                   read_only=True,
                                                   view_name="article-detail")
    
    # articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Journalist
        fields = "__all__"

```

- In views.py

```python

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from news.models import Article, Journalist
from news.api.serializers import ArticleSerializer, JournalistSerializer


class JournalistListCreateAPIView(APIView):
    def get(self, request):
        journalists = Journalist.objects.all()
        serializer = JournalistSerializer(journalists, 
                                          many=True,
                                          context={"request": request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = JournalistSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ArticleListCreateAPIView(APIView):
    
    def get(self, request):
        articles = Article.objects.filter(active=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ArticleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ArticleDetailAPIView(APIView):
    def get_object(self, pk):
        article = get_object_or_404(Article, pk=pk)
        return article

    def get(self,request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

```

- In urls.py

```python
from django.urls import path
from news.api.views import ArticleListCreateAPIView,\
                           ArticleDetailAPIView,\
                           JournalistListCreateAPIView
# from news.api.views import article_list_create_api_view,\
#                            article_detail_api_view

urlpatterns = [
    path("articles/", 
         ArticleListCreateAPIView.as_view(),
        name="article-list"),

    path("articles/<int:pk>", 
         ArticleDetailAPIView.as_view(), 
         name="article-detail"),

    path("journalists/", 
         JournalistListCreateAPIView.as_view(),
         name="journalist-list"),
]    
```


- Do not forget to register the new model created

```python

from django.contrib import admin
from .models import Article, Journalist
# Register your models here.

admin.site.register(Article)
admin.site.register(Journalist)

```

