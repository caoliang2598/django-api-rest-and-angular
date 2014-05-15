from django.contrib import admin

from .models import User, Post, Photo, Plan, Activity


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Plan)
admin.site.register(Activity)