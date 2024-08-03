from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Post, Follow, Like


def index(request):
    current_user = request.user
    posts = Post.objects.all().order_by("id").reverse()

    # Display 10 posts at most per page
    paginator = Paginator(posts, 10)
    page = request.GET.get("page")
    page_posts = paginator.get_page(page)

    likes = Like.objects.all()

    # Get liked posts of the current_user
    liked = []
    for like in likes:
        if current_user.id == like.liker.id:
            liked.append(like.post.id)

    return render(request, "network/index.html", {
        "current_user": current_user,
        "posts": page_posts,
        "liked": liked
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == "POST":
        current_user = User.objects.get(pk=request.user.id)
        content = request.POST["new_content"]
        post = Post(poster=current_user, content=content)
        post.save()
    return HttpResponseRedirect(reverse("index"))


def profile(request, id):
    current_user = request.user
    profile_user = User.objects.get(pk=id)
    profile_posts = Post.objects.filter(poster=profile_user).order_by("id").reverse()

    # Get profile_user followers and following
    profile_followers = Follow.objects.filter(following=profile_user)
    profile_following = Follow.objects.filter(follower=profile_user)

    # Attempts to find whether current_user follows profile_user
    try:
        check_following = profile_followers.filter(follower=User.objects.get(pk=current_user.id))
        if check_following:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False

    # Display 10 posts at most per page
    paginator = Paginator(profile_posts, 10)
    page = request.GET.get("page")
    profile_page_posts = paginator.get_page(page)

    # Get liked posts of the current_user
    likes = Like.objects.all()
    liked = []
    for like in likes:
        if current_user.id == like.liker.id:
            liked.append(like.post.id)

    return render(request, "network/profile.html", {
        "current_user": current_user,
        "profile_user": profile_user,
        "profile_posts": profile_page_posts,
        "profile_followers": profile_followers,
        "profile_following": profile_following,
        "is_following": is_following,
        "liked": liked
    })

@login_required
def unfollow(request, id):
    current_user = User.objects.get(pk=request.user.id)
    follow_user = User.objects.get(pk=id)
    follow = Follow.objects.get(follower=current_user, following=follow_user)
    follow.delete()
    return HttpResponseRedirect(reverse(profile, kwargs={"id": id}))


@login_required
def follow(request, id):
    current_user = User.objects.get(pk=request.user.id)
    follow_user = User.objects.get(pk=id)
    follow = Follow(follower=current_user, following=follow_user)
    follow.save()
    return HttpResponseRedirect(reverse(profile, kwargs={"id": id}))


@login_required
def following(request):
    current_user = User.objects.get(pk=request.user.id)
    following_users = Follow.objects.filter(follower=current_user)
    posts = Post.objects.all().order_by("id").reverse()

    # Gets the posts of the current_user following
    following_posts = []

    for post in posts:
        for following_user in following_users:
            if post.poster == following_user.following:
                following_posts.append(post)

    # Display 10 posts at most per page
    paginator = Paginator(following_posts, 10)
    page = request.GET.get("page")
    following_page_posts = paginator.get_page(page)

    # Get liked posts of the current_user
    likes = Like.objects.all()
    liked = []
    for like in likes:
        if current_user.id == like.liker.id:
            liked.append(like.post.id)

    return render(request, "network/following.html", {
        "following_posts": following_page_posts,
        "liked": liked
    })


@csrf_exempt
@login_required
def edit(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=id)
        edit_post.content = data["content"]
        edit_post.save()
    return JsonResponse({"message": "Changed!", "data": data["content"]})


@csrf_exempt
@login_required
def like(request, id):
    current_user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=id)
    like = Like(liker=current_user, post=post)
    like.save()
    post.likes += 1
    post.save()
    return JsonResponse({"message": "Liked!", "data": post.likes})

@csrf_exempt
@login_required
def unlike(request, id):
    current_user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=id)
    like = Like.objects.filter(liker=current_user, post=post)
    like.delete()
    post.likes -= 1
    post.save()
    return JsonResponse({"message": "Unliked!", "data": post.likes})
