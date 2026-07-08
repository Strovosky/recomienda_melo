from django.contrib import admin
from .models import Place, Review, Like, Category

admin.site.register(Place)
admin.site.register(Review)
admin.site.register(Like)
admin.site.register(Category)
