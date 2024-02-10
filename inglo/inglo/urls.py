from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('issues/', include('issues.urls')),
    path('posts/', include('posts.urls')),
    path('sketches/', include('sketches.urls')),
]
