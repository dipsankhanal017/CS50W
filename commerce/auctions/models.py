from django.contrib.auth.models import AbstractUser
from django.db import models
from autoslug import AutoSlugField



class User(AbstractUser):
    ...


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    imageurl = models.URLField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings')
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, related_name='listings', on_delete=models.CASCADE)
    title_slug = AutoSlugField(populate_from='title', unique=True, always_update=False, null=False, blank=True)
    soldto = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank="True")


    def __str__(self):
        return self.title

class Bids(models.Model):
    title = models.ForeignKey(Listing, on_delete=models.CASCADE)
    current_bid = models.FloatField()
    current_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_bidder", null=True)

    def __str__(self):
        return f"{self.current_bidder} bids ${self.current_bid} on {self.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return f"Comment by {self.user} on {self.listing} | {self.comment}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, related_name='watchlist', on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name='watched_by', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} is watching {self.listing}"
