from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods

def index(request):
    return render(request, "posts/index.html")


def post_list(request):
    posts = Post.objects.all().order_by("-pk")
    context = {
        "posts": posts
    }
    return render(request, "posts/post_list.html", context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:post_detail", post.pk)
        
    else:
        form = PostForm
    
    context = {"form": form}
    return render(request, "posts/post_create.html", context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    comments = post.comments.all().order_by("-pk")
    like = post.like_users.all()
    context = {
        "post": post,
        "comment_form": comment_form,
        "comments": comments,
        "like": like,
    }
    return render(request, "posts/post_detail.html", context)


@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        if post.author == request.user:
            post.delete()
    return redirect("posts:post_list")


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                return redirect("posts:post_detail", post.pk)
        else:
            form = PostForm(instance=post)
    context = {
        "form": form,
        "post": post,
    }
    return render(request, "posts/post_update.html", context)


@require_POST
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return redirect("posts:post_detail", post.pk)


@require_POST
def comment_delete(request, pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
    return redirect("posts:post_detail", pk)


def comment_update(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        if request.method == "POST":
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect("posts:post_detail", pk)
        else:
            form = CommentForm(instance=comment)
        
        context = {
            "form": form,
            "post": comment.post,
            "comment": comment,
        }
        return render(request, "posts/comment_update.html", context)


@require_POST
def like(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if post.like_users.filter(pk=request.user.pk).exists():
            post.like_users.remove(request.user)
        else:
            post.like_users.add(request.user)
        return redirect("posts:post_detail", pk)
    return redirect("users:login")