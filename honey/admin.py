from django.contrib import admin

from honey.models import Group, Honey, Stock, Order, Feedback

# Register your models here.
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Honey)
class HoneyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group', 'count']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group', 'count']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group', 'comment']