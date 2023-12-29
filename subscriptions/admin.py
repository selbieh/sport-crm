from django.contrib import admin

from subscriptions.models import Subscription, FreezingRequest

# Register your models here.
admin.site.register(Subscription)
admin.site.register(FreezingRequest)
