from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'datetime_modified', 'id')

# admin.site.register(Post,PostAdmin)
