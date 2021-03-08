from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm,Textarea
from .models import User,Posts,Follower,Like
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class PostsForm(ModelForm):
    
    class Meta:
        model = Posts
        fields = ['text']
        labels ={
            'text': False,
        }
        widgets = {
            'text': Textarea(attrs={'cols': 40, 'rows': 10}),
        }
        
        


def index(request):
    
    
    if request.method == 'GET':

        posts = Posts.objects.all()
        paginator = Paginator(posts, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        
        return render(request,"network/index.html",{
            'form':PostsForm(),
            'page_obj':page_obj
        })

    if request.method == 'POST':

        if request.user.is_authenticated:
            form = PostsForm(request.POST)
            if form.is_valid():
                form = form.cleaned_data
            
            post = Posts.objects.create(author = request.user, text = form['text'] )
            post.save() 
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('login'))



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
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

def profile(request,id):

    if request.method == "GET":
        user = User.objects.get(pk=id)
        current_user = request.user
        
        #get user posts and followers
        posts = Posts.objects.filter(author=user)

        followers = Follower.objects.filter(followed=user).count()
        following = Follower.objects.filter(follows=user).count()

        paginator = Paginator(posts, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        
        #bt = 0 //the follow button should not exist, bt = 1 // follow button, bt = 2 // unfollow button
        bt = 0
        if user.username != current_user.username:
            bt = 1
        if Follower.objects.filter(follows=current_user, followed=user):
            bt = 2
        
        
        return render(request, "network/profile.html",{
            "author":user,
            "page_obj":page_obj,
            "bt":bt,
            "followers":followers,
            "following":following


        })
    if request.method == "POST":

        follower = request.user
        followed = User.objects.get(pk=id)

        if request.POST.get('f'):
            
            follow = Follower.objects.create(follows=follower, followed=followed)
            follow.save()
        
        if request.POST.get ('u'):
            follow =  Follower.objects.filter(follows=follower, followed=followed)
            follow.delete()

        return HttpResponseRedirect(reverse("profile", args=[id]))

@login_required(login_url='login')
def following(request):

    posts = []
    for f in Follower.objects.filter(follows=request.user):
        for post in Posts.objects.filter(author=f.followed):
            posts.append(post)

    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render (request, "network/following.html",{
        "page_obj":page_obj
    })

def edit(request, id):

    txt = request.POST.get(f'edit+{id}')
    if request.method == "POST":
        Posts.objects.filter(pk=id).update(text=txt)
    return HttpResponseRedirect(reverse("profile",args=[request.user.id]))


@csrf_exempt

def like(request):

    if request.method == "POST":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            id = data['id']
            if Like.objects.filter(author=request.user,post = Posts.objects.filter(pk=id)[0]):
                Like.objects.filter(author=request.user,post = Posts.objects.filter(pk=id)[0])[0].delete()
                return JsonResponse({"message":"unliked post"},status=201)
            else:
                like = Like.objects.create(author=request.user,post = Posts.objects.filter(pk=data['id'])[0])
                like.save()
                return JsonResponse({"message":"liked post"},status=201)
        else:
            return JsonResponse({"message":"redirect"},status=201)
        

@csrf_exempt
def like_nr(request,post_id):
    
    
    post  = Posts.objects.get(pk=post_id)
    like_count = Like.objects.filter(post = post )
    
    #if the user has alleady like this post the bt should be "unlike"
    dislike = False
    for post in like_count:
        if request.user.username == post.author.username:
            dislike = True

    like_count = like_count.count()
    data = {
        "like_nr": like_count,
        "bt_status": dislike
    }
    
    if request.method == "GET":
        return JsonResponse(data,status=201,safe=False)

    


