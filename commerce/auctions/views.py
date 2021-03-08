from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm,forms,Textarea
from django import forms
from django.contrib.auth.decorators import login_required

from .functions import *
from .models import * 

class ListingForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={
        'cols': 200,
        'rows': 3,
        'style': 'width: 100%',
        'class': 'form-control'
    }))
    class Meta:
        model = Listing
        fields = ['title', 'price', 'link', 'category']
        

def index(request):

    current_user = request.user
    listings = Listing.objects.filter(status=True)
    current_price = price(listings)
    
    return render(request, "auctions/index.html", {
        "listings":listings,
        "bids":current_price
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

#make a new listing
@login_required(login_url='login')
def listing(request):

    if request.method == "GET":
        return render(request, "auctions/listing.html", {
            "forms": ListingForm()
        })
    
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
             form = form.cleaned_data
             
        #append the form to the db
        listing = Listing(title=form['title'], price=form['price'],description=form['description'],link=form['link'],author=request.user,category=form['category'])
        listing.save()
        bid = Bids(bid = form['price'],listing=listing,author=request.user)
        bid.save()
        return HttpResponseRedirect(reverse("index"))

def page(request,pk):

    #get the listing by pk and find the highest bid aka current price
    listing = Listing.objects.filter(pk=pk)
    listing=listing[0]
    bid=Bids.objects.filter(listing=listing).order_by('-bid')
    bid=bid[0]
    
    #look to see if the listing is in the watchlist model that matches the current user
    watchlist = 0
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user).filter(listing=listing)
        if watchlist:
            watchlist=watchlist[0]
    
    user=request.user

    coms = Comments.objects.filter(listing=listing)
    return render(request, "auctions/page.html", {
        "listing":listing,
        "bid":bid, 
        "user":user,
        "watchlist":watchlist,
        "comments":coms
    })


def listing_actions(request,pk):
    
    if request.POST.get('close'):
        Listing.objects.filter(pk=pk).update(status=False)


    if request.POST.get('add_watch'):
        listing = Listing.objects.filter(pk=pk)
        listing = listing[0]
        watchlist = Watchlist(listing=listing,user=request.user)
        watchlist.save()
    
    if request.POST.get("rem_watch"):
        listing = Listing.objects.filter(pk=pk)
        listing = listing[0]
        Watchlist.objects.filter(user=request.user).filter(listing=listing).delete()
        
    if request.POST.get("new_bid"):
        new_bid = request.POST.get("bid")
        
        if not new_bid:
            return HttpResponse("Must type a valid bid")
        
        if float (new_bid) <= Bids.objects.filter(listing__pk=pk).order_by('-bid')[0].bid:
            return HttpResponse("Must bid higher than the current price")

        bid = Bids(bid=new_bid,listing=Listing.objects.filter(pk=pk)[0],author=request.user)
        bid.save()

    if request.POST.get ("new_com"):
        new_com = request.POST.get("com")
        
        if  not new_com:
            return HttpResponse("Must type a comment")
        com = Comments(comment=new_com,listing=Listing.objects.filter(pk=pk)[0])
        com.save()

    return HttpResponseRedirect(reverse("page", args=[pk]))

@login_required(login_url='login')
def watchlist(request):

    user = request.user
    watchlist=Watchlist.objects.filter(user=user)

    
    return render(request,"auctions/watchlist.html", {
        "watchlist":watchlist
       
    })



def cat(request):

    if request.method == "GET":
        
        #look for the categories of all active listings and use a set to append only once
        cat = set()
        listings = Listing.objects.filter(status=True)
        for listing in listings:
            cat.add(listing.category)
        
        return render(request,"auctions/cat.html", {
            "cat":cat
            })

    if request.method == "POST":

        cat = request.POST.get('cat')
        cat = Listing.objects.filter(category=cat).filter(status=True)
        
        current_price = price(cat)
    return render(request, "auctions/index.html", {
        "listings":cat,
        "bids":current_price
    })
    