from django.contrib import admin
from .models import Category, Listing, User, Comment, Watchlist, Bids

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Bids)

