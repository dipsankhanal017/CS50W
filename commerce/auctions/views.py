from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Category, Bids, Watchlist

def index(request):
    listing = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {'listing': listing})

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

@login_required
def listing_details(request, slug):
    product = Listing.objects.get(title_slug = slug)
    comments = Comment.objects.filter(listing = product)
    bid = Bids.objects.filter(title=product).order_by('-current_bid').first()
    username = request.user.username
    try:
        watchlist = Watchlist.objects.get(listing=product, user=request.user) 
        print(watchlist.user)
    except Watchlist.DoesNotExist:
        watchlist = None 


    minimum = bid.current_bid + 0.01
    if request.method == "POST":
        if 'submit_comment' in request.POST:
            comment = request.POST["comment"]
            title = request.POST["title"]

            user = User.objects.get(username = username)
            title = Listing.objects.get(title = title)

            comments1 = Comment(user = user, listing = title, comment = comment)
            comments1.save()
        elif 'submit_bid' in request.POST:
            bid = request.POST["bid-amount"]
            bid = float(bid)

            user = User.objects.get(username = username)
            title = Listing.objects.get(title = product)

            bid1 = Bids(title = title, current_bid = bid, current_bidder = user)
            bid1.save()
            bid = Bids.objects.filter(title=product).order_by('-current_bid').first()
            minimum = bid.current_bid + 0.01
        elif 'closebids' in request.POST:
            soldto = request.POST['newowner']
            product.soldto = User.objects.get(username = soldto)
            product.active = False
            product.save()
        elif 'removewatchlist' in request.POST:
            user = User.objects.get(username = username)
            title = Listing.objects.get(title = product)
            watch = Watchlist.objects.get(listing=title, user=user)
            watch.delete()
            return HttpResponseRedirect(reverse("watchlist"))

        elif 'addwatchlist' in request.POST:
            user = User.objects.get(username = username)
            title = Listing.objects.get(title = product)
            watch = Watchlist(listing = title, user = user)
            watch.save()
            return HttpResponseRedirect(reverse("watchlist"))
      
    if username == product.owner.username:
        isowner = True
    else: 
        isowner = False

    if product.soldto:
        message = True
    else:
        message = False


    return render(request, "auctions/productdetails.html", {
        'product': product,
        'comments': comments,
        'bids': bid,
        'minimum': minimum, 
        'isowner': isowner,
        'message': message,
        'username':username,
        'watchlist': watchlist,
    })

@login_required
def createlisting(request):
    categories = Category.objects.all()
    username = request.user.username
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        startingbid = request.POST["startingbid"]
        categoryname = request.POST["category"]
        ownername = request.POST["ownername"]

        category = Category.objects.get(name=categoryname)
        owner = User.objects.get(username=ownername)



        listing = Listing(
            title=title,
            description=description,
            imageurl=imageurl,
            category=category,
            owner=owner
        )
        listing.save()

        initial_bid = Bids(
            title=listing,
            current_bid=startingbid,
            current_bidder=owner
        )
        initial_bid.save()

    return render(request, "auctions/createlisting.html",{
        "categories":categories,
        "username": username,
        }
    )

def categoriespage(request):
    listing = Listing.objects.filter(active=True)
    categories = Category.objects.all()
    if request.method == "POST":
        category = request.POST["category"]
        category = Category.objects.get(name=category)

        listing = Listing.objects.filter(active=True, category = category)
    return render(request, "auctions/categories.html", {
        "listing":listing,
        "categories": categories,
    })

@login_required
def watchlists(request):
    user = request.user.username
    user = User.objects.get(username = user)
    watch = Watchlist.objects.filter(user = user)
    return render(request, "auctions/watchlist.html",{
        "watchlist": watch,
    })