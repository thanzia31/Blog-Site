from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField



# Create your models here.

class authors(models.Model):
    username=models.CharField(max_length=30,unique=True)
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)

    profile=models.ImageField()
    bio=models.CharField(max_length=100)
    link=models.URLField()
    email=models.EmailField()

    def __str__(self):
        return str(self.username)
    

class category(models.Model):
    title=models.CharField(max_length=70,unique=True)
    slug=AutoSlugField(populate_from='title',unique=True)

    def __str__(self):
        return self.title

class post(models.Model):
    title=models.CharField(max_length=50)
    content=RichTextUploadingField()
    
    thumbnail=models.ImageField(upload_to='images/')
    slug=AutoSlugField(populate_from='title',unique=True)
    categories= models.ForeignKey(
        to=category,
        related_name="post",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    author=models.ForeignKey(to=authors,to_field='username', on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name='blog_posts',blank=True,null=True)
    like_field=models.BooleanField(default=False)
    userlikes=models.JSONField(blank=True,default=dict)
   
    
    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title
    
    

