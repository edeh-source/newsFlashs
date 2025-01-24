from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.db.models import Count
from django.contrib import messages
from news.forms import CommentForm, ReplyForm
from .models import Category, Author, Post, Reply, Comment
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger    
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchHeadline, SearchRank
from taggit.models import Tag
from django.shortcuts import redirect






class PostHomePage(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post/index.html'
    
    def get_queryset(self):
        return Post.objects.filter(category__name="Trending News", active=True).order_by('-publish')[:5]
    
    
def get_culture_category(request):
    culture = Post.objects.filter(category__name="Culture", active=True).order_by('-publish')[:1]
    return {'culture': culture}    


def get_all_posts(request):
    all_post = Post.objects.filter(active=True).order_by('-publish')[:9]
    return {'all_post': all_post}

def get_one_trending_news(request):
    one_trend_news = Post.objects.filter(category__name='Trending News', active=True).order_by('-publish').first()
    return {'one_trend_news': one_trend_news}     

def get_all_trending_news(request):
    all_trend_news = Post.objects.filter(category__name='Trending News', active=True).order_by('-publish')[:6]
    return {'all_trend_news': all_trend_news}


def get_one_buisness_news(request):
    one_buisness_news = Post.objects.filter(category__name='Business and Finance', active=True).order_by('-publish').first()
    return {'one_buisness_news': one_buisness_news}


def get_all_buisness_news(request):
    all_buisness_news =  Post.objects.filter(category__name='Business and Finance', active=True).order_by('-publish')[:6]
    return {'all_buisness_news': all_buisness_news}


def get_one_sports_news(request):
    one_sports_news = Post.objects.filter(category__name='Sports', active=True).order_by('-publish').first()
    return {'one_sports_news': one_sports_news}
    
    
def get_all_sports_news(request):
    all_sports_news =  Post.objects.filter(category__name='Sports', active=True).order_by('-publish')[:6]
    return {'all_sports_news': all_sports_news}  


def get_one_international_news(request):
    one_international_news = Post.objects.filter(category__name='Foreign News', active=True).order_by('-publish').first()
    return {'one_international_news': one_international_news}


def get_all_international_news(request):
    all_international_news = Post.objects.filter(category__name='Foreign News', active=True).order_by('-publish')[:6]
    return {'all_international_news': all_international_news}


def get_one_technology_news(request):
    one_technology_news = Post.objects.filter(category__name='Technology', active=True).order_by('-publish').first()
    return {'one_technology_news': one_technology_news}

def get_all_technology_news(request):
    all_technology_news = Post.objects.filter(category__name='Technology', active=True).order_by('-publish')[:6]
    return {'all_technology_news': all_technology_news}


def get_one_health_news(request):
    one_health_news = Post.objects.filter(category__name='Health', active=True).order_by('-publish').first()
    return {'one_health_news': one_health_news}


def get_all_health_news(request):
    all_health_news = Post.objects.filter(category__name='Health', active=True).order_by('-publish')[:6]
    return {'all_health_news': all_health_news}

def get_post_details(request, slug, year, month, day):
    post = get_object_or_404(Post, slug=slug, publish__year=year, publish__month=month, publish__day=day, active=True)
    request.session['post_title'] = post.name
    post.views += 1
    post.save()
    related_tags = post.tags.all()
    comments = post.comments.filter(active=True)
    user = request.user
    similiar_post = None
    comment = None
    reply = None
    replies = None
    if reply:
        reply = get_object_or_404(Reply, id=reply)
        replies = reply.comment.filter(active=True)
        
    else:
        pass    
        
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            messages.success(request, 'COMMENT SUBMITTED SUCCESFULLY')
        else:
            messages.error(request, 'CORRECT THE ERROR BELOW') 
    else:
        form = CommentForm()  
        post_tags_ids = post.tags.values_list('id', flat=True)
        similiar_post = Post.objects.filter(tags__in=post_tags_ids, active=True).exclude(id=post.id)
        similiar_post = similiar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', 'active')[:4]
        

    return render(request, 'post/single-post.html', {'post': post, 'related_tags': related_tags, 'form': form, 'comment': comment, 'comments': comments, 'user': user, 'replies': replies, 'similiar_post': similiar_post}) 


def get_all_categories(request):
    category = Category.objects.all()
    return {'category': category}



def post_categories(request, slug):
    """
    A View That gets a category slug and filter the database to get all posts from the category
    """
    
    category_list = get_object_or_404(Category, slug=slug)
    post_category_list = Post.objects.filter(category=category_list, active=True).order_by('-publish')
    paginator = Paginator(post_category_list, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'post/category.html', {'page_obj': page_obj, 'category_list': category_list})
    
    
    
    
    
def get_pagination_range(current_page, total_pages, delta=2):
    """
    Generate a pagination range with ellipses:
    - `current_page`: The currently active page.
    - `total_pages`: Total number of pages.
    - `delta`: Number of pages to show around the current page.
    """
    if total_pages <= 7:
        return list(range(1, total_pages + 1))

    pages = []

    # Always show the first page
    pages.append(1)

    # Add ellipsis if there’s a gap between the first pages and the current page range
    if current_page > delta + 2:
        pages.append("...")

    # Add pages around the current page
    start = max(2, current_page - delta)
    end = min(total_pages - 1, current_page + delta)
    pages.extend(range(start, end + 1))

    # Add ellipsis if there’s a gap between the current page range and the last pages
    if current_page < total_pages - delta - 1:
        pages.append("...")

    # Always show the last page
    pages.append(total_pages)

    return pages


def authors_post(request, username):
    author = get_object_or_404(Author, user__username=username)
    post_list = Post.objects.filter(author=author, active=True).order_by('-publish')
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Use the custom pagination range
    pagination_range = get_pagination_range(page_obj.number, paginator.num_pages)

    return render(
        request,
        'post/authors.html',
        {
            'page_obj': page_obj,
            'author': author,
            'pagination_range': pagination_range,
        },
    )
    
    



def get_recent_post(request):
    recent_post = Post.objects.filter(active=True).order_by('-publish')[:7]
    return {'recent_post': recent_post}


def post_search(request):
    query = request.GET.get("query", "")
    
    if not query:
        # Handle the case where there is no query
        return render(request, 'post/search-result.html', {'page_obj': [], 'query': query })

    search_vector = SearchVector("name", "text")
    search_query = SearchQuery(query)
    search_headline = SearchHeadline("text", search_query)

    post_list = Post.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).annotate(headline=search_headline).filter(search=search_query, active=True).order_by("rank", '-publish')

    # Debugging: Check the number of posts found
    print(f"Number of posts found: {post_list.count()}")

    paginator = Paginator(post_list, 3)  # Show 3 posts per page
    page_number = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)  # Redirect to the last page if the page number is out of range

    return render(request, 'post/search-result.html', {'page_obj': page_obj, 'query': query })


class Tag_Detail(ListView):
    model = Post
    template_name = 'post/tag.html'
    context_object_name = 'tags'
    paginate_by = 1

    def get_queryset(self):
        tags = get_object_or_404(Tag, slug=self.kwargs['slug'])
        post_tags = Post.objects.filter(tags=tags)
        return post_tags



def reply_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    reply = None
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
           reply = form.save(commit=False)
           reply.user = request.user
           reply.comment = comment
           reply.save()
           post = comment.post
           messages.success(request, 'Replied Succesfully')
           return redirect('post_details',  slug=post.slug, year=post.publish.year, month=post.publish.month, day=post.publish.day)
        else:
            messages.error(request, 'Correct The Error Below')
    else:
        form = ReplyForm()
    return render(request, 'post/reply.html', {'reply': reply, 'form': form })   




def most_popular_post(request):
    posts = Post.objects.order_by('-views')[:5]
    most_popular_posts = list(posts)
    return {'most_popular_posts': most_popular_posts}



def get_latest_posts(request):
    all_latest_post = Post.objects.filter(active=True).order_by('-publish')[:5]
    return {'all_latest_post': all_latest_post}       
             
             
def trending_news(request):
    trend_category = Category.objects.get(name='Trending News')
    post_trend_news = Post.objects.filter(category=trend_category, active=True).order_by('-publish')[:5]
    return {'post_trend_news': post_trend_news, 'trend_category': trend_category }             