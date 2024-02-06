from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('issues/', include('issues.urls')),
    path('posts/', include('posts.urls')),
    path('sketches/', include('sketches.urls')),
    path('commons/', include('commons.urls')),

]
