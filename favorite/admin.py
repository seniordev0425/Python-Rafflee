from django.contrib import admin
from .models import Favorite, Highlight, Subscription
from favorite.django_admin.favorite_admin import FavoriteAdmin
from favorite.django_admin.highlight_admin import HighlightAdmin
from favorite.django_admin.subscriptions_admin import SubscriptionsAdmin

admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Highlight, HighlightAdmin)
admin.site.register(Subscription, SubscriptionsAdmin)
