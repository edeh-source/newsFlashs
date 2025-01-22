from django.db import models
from django.contrib.auth import get_user_model
import uuid
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from embed_video.fields import EmbedVideoField
from taggit.managers import TaggableManager
User = get_user_model()
from django_resized import ResizedImageField


class Category(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False, null=False, blank=False)
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256, db_index=True, unique=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
    def get_absolute_url(self):
        return reverse("categories_post", args=[self.slug])
    
    
    class Meta:
        ordering = ["-created", ]
        verbose_name = "category"
        verbose_name_plural = "categories"
    
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)    
            
    

class Author(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    about =  RichTextField(blank=True)
    facebook_link = models.URLField(blank=True)
    whatsapp_link = models.URLField(blank=True)
    reddit_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.name
    
    
    def get_authors_post_url(self):
        return reverse('author_post', args=[self.user.username])
    
    

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    name = models.CharField(max_length=256, db_index=True, unique=True)
    slug = models.SlugField(max_length=256, db_index=True, unique_for_date='publish', null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    publish = models.DateTimeField(default=timezone.now)
    image =  ResizedImageField(size=[900, 630], crop=['middle', 'center'], quality=85, upload_to='post_images/')
    image_description = models.CharField(max_length=100, blank=True)
    text = RichTextField()
    views = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    tags = TaggableManager(blank=True)
    videos = EmbedVideoField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    news_link = models.URLField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    
    
    def get_absolute_url(self):
        return reverse("post_details", args=[self.slug, self.publish.year, self.publish.month, self.publish.day])
    
    
    
    
    
      
      
      
class Comment(models.Model):
    post = models.name = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, related_name='comments', on_delete=models.CASCADE, default='ba94a1b9-8dce-4e5c-a0df-be383b13a070')
    name = models.CharField(max_length=80, blank=True, null=True)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post} on {self.body}'



class Reply(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Reply by {self.user} on {self.comment} '    