from django.contrib import admin
from .models import Post, Author, Category



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created', 'updated']
    list_filter = ['name', 'slug', 'created', 'updated']
    

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user', 'active', 'created', 'updated', 'whatsapp_link', 'facebook_link']    
    list_filter = ['user', 'active', 'created', 'updated', 'whatsapp_link', 'facebook_link']    
    
    
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display =  ['category','name', 'slug', 'author', 'active','views','publish','active', 'created']  
    list_filter =  ['category', 'name', 'slug', 'author', 'active', 'views','publish','active', 'created'] 
    prepopulated_fields = {'name': ('slug',)}
    list_per_page = 10 
        