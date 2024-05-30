from django.contrib import admin
from blogapp.models import post,authors,category

# Register your models here.
admin.site.register(post)
admin.site.register(authors)
admin.site.register(category, admin.ModelAdmin)


