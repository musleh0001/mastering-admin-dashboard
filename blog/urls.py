from django.contrib import admin
from django.urls import path

admin.site.site_header = "Super Blog admin"
admin.site.site_title = "Super Blog Admin"
admin.site.index_title = "Super Blog Administration"

urlpatterns = [
    path("admin/", admin.site.urls),
]
