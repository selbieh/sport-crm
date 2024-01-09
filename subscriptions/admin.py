from django.contrib import admin

from subscriptions.models import Subscription, FreezingRequest, SubscriptionAttendance

# Register your models here.
admin.site.register(Subscription)
admin.site.register(FreezingRequest)
admin.site.register(SubscriptionAttendance)
