from django.contrib import admin
from .models import User,Blog,Tag
# Register your models here.

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Tag)
