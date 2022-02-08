from sre_parse import CATEGORIES
from unicodedata import name
from django.shortcuts import render
from .forms import CommentForm, PostForm
from blog.models import Post, Comment
from django.http import HttpResponseRedirect

def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {
        "posts": posts,
    }
    return render(request, "blog_index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "blog_category.html", context)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }

    return render(request, "blog_detail.html", context)

def blog_new_post(request):
 
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = Post(
                title=form.cleaned_data["title"],
                body=form.cleaned_data["body"]
            )
            post.save()
            return HttpResponseRedirect('/blog')
            
    else:

        return render(request, "blog_new_post.html", {'form': form})

    

    
