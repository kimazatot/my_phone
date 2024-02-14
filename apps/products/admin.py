from django.contrib import admin
from .models import *
from apps.review.models import *


class ReviewInline(admin.TabularInline):
    model = Review


class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
