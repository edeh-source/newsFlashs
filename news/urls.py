from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostHomePage.as_view(), name='home'),
    path('detail/<slug:slug>/<int:year>/<int:month>/<int:day>/', views.get_post_details, name='post_details'),
    path('category/<slug:slug>/', views.post_categories, name='categories_post'),
    path('authors/<str:username>/', views.authors_post, name='author_post'),
    path('search/', views.post_search, name='post_search'),
    path('tags/<slug:slug>/', views.Tag_Detail.as_view(), name='tag_details'),
    path('comment_reply/<int:id>/', views.reply_comment, name='comment_reply'),
]